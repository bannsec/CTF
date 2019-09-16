#!/usr/bin/env python

from revenge import Process

p = Process("./beleaf", resume=False)


# Correct output table
mem = p.memory['beleaf:0x2014E0']
addr = mem.address

correct = []

for i in range(0x21):
    correct.append(p.memory[addr + (i*8)].int64)

l = {}
l2 = {}

lookup = p.memory['beleaf:0x7FA']

for i in range(256):
    x = lookup(i)
    l[i] = x
    l2[x] = i

''.join(chr(l2[x]) for x in correct)
# 'flag{we_beleaf_in_your_re_future}'

