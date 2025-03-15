from pwn import *

io = process('sh')
io.sendline(b'python3 server.py')
encrypted_flag = str(io.recvline()[len('encrypted flag: '):-1], 'utf-8')
print('encrypted_flag:',encrypted_flag)
print(encrypted_flag)
io.recvuntil(b'> ')
vec = '0123456789abcdef'
io.sendline(bytes(vec,'utf-8'))
encrypted_vec = str(io.recvline()[1:],'utf-8')
io.recvuntil(b'> ')
rev_sbox = {encrypted_vec[i]:vec[i] for i in range(16)}
print('reverse sbox:',rev_sbox)
flag_hex = ''.join([rev_sbox[c] for c in encrypted_flag])
print("flag (hex):", flag_hex)
flag = str(bytes.fromhex(flag_hex),'utf-8')
print("flag:", flag)