#!/usr/bin/env python

import r2pipe
from base64 import b64decode, b64encode
from pwn import p32
from itertools import product

alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

r2 = None

def open():
    global r2
    r2 = r2pipe.open("./product_key")
    r2.cmd('')

def close():
    global r2
    r2.quit()
    r2 = None

def show_decode(key):
    assert len(key) == 39
    open()
    r2.cmd('ood ' + key)
    r2.cmd('dbm product_key 0x00000957')
    r2.cmd('dc')
    val = b64decode(r2.cmd('p6e 0x14 @ rbp'))
    close()
    return val

def show_decode_no_restart(key):
    """Don't restart bin, just reset ip."""

    print("Trying: " + key)

    assert len(key) == 39

    if r2 == None:
        open()
        r2.cmd('ood ' + key)
        r2.cmd('dbm product_key 0xb60')
        r2.cmd('dc')

    else:
        base_addr = next(x for x in r2.cmdj('dmmj') if x['file'].endswith('product_key'))['addr']
        r2.cmd('dr rip={}'.format(base_addr + 0xb60))

    r2.cmd('dbm product_key 0x00000c74') # Break at end of decode

    # Write in the key
    r2.cmd('w6d {} @ rdi'.format(b64encode(key.replace('-','').encode()).decode()))

    # Clear rsi
    r2.cmd('w6d {} @ rsi'.format(b64encode(b'\x00'*16).decode()))

    r2.cmd('dc')
    r2.cmd('db-*')

    val = b64decode(r2.cmd('p6e 0x14 @ rbp'))
    return val

# AAAA-AAAA-AAAA-AAAA-AAAA-AAAA-AAAA-AAAA
# Compresses to 20 char from decode
# last 4 of those 20 char is checksum


def calculate_checksum(key):
    """Use the program to generate our checksum."""

    assert len(key) == 16 

    if type(key) is str:
        key = key.encode()

    open()
    r2.cmd('ood AAAA-AAAA-AAAA-AAAA-AAAA-AAAA-AAAA-AAAA') # Actual value doesn't matter
    r2.cmd('dbm product_key 0x00000960')
    r2.cmd('dc')

    r2.cmd('db-*') # Make sure we don't hit this breakpoint again

    r2.cmd('w6d {} @ rdx'.format(b64encode(key).decode()))
    r2.cmd('dbm product_key 0x976')
    r2.cmd('dc')
    checksum = int(r2.cmd('dr eax'),16)
    close()
    return checksum

def concat_key(key):
    assert type(key) is list

    key_str = ''
    for i in range(0, len(key), 4):
        key_str += key[i] + key[i+1] + key[i+2] + key[i+3] + '-'

    return key_str.strip('-')

checksum = p32(calculate_checksum('i-am-misakiakeno'))

goal = b'i-am-misakiakeno' + checksum

discovered = 0
key = ['A']*32

# NOTE: This ended up being WAY too slow...
for x in product(alphabet, alphabet):
    # Update our key
    key[discovered] = x[0]
    key[discovered+1] = x[1]

    out = show_decode(concat_key(key))
    if out[int(discovered/2)] == goal[int(discovered/2)]:
        discovered += 2
        break

