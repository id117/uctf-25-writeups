from pwn import *

io = process('sh')
io.sendline(b'python3 server.py')
size = int(str(io.recvline()[len('box size: '):-1], 'utf-8'))
print('size:', size)
if size>154:exit()
encrypted_flag = str(io.recvline()[len('encrypted flag: '):-1], 'utf-8')
print('encrypted_flag:',encrypted_flag)
io.recvuntil(b'> ')
vec154='0123456789abcdefghijklmnopqrstuvwxyzABVDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*(),-=+`/\\~:"\'<>?абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ№|'
vec = vec154[:size]
print('vec:',vec)
io.sendline(bytes(vec,'utf-8'))
encrypted_vec = str(io.recvline()[:-1],'utf-8')
print('encrypted vec:', encrypted_vec)
io.recvuntil(b'> ')
rev_pbox = [encrypted_vec.index(vec[i]) for i in range(size)]
print('reverse pbox:',rev_pbox)
def pbox(buf, box):
    return ''.join([buf[i] for i in box])
def encrypt(buf, box, size):
    return ''.join([pbox(buf[i:i+size],box) for i in range(0,len(buf),size)])
flag = encrypt(encrypted_flag, rev_pbox, size)
print("flag:", flag)