from pwn import *
flag = ''

GREEN = '\033[92m'
YELLOW = '\033[33m'
RED = '\033[91m'
BLUE = '\033[94m'
ENDC = '\033[0m'

def communicate(io,payload):
    io.sendline(bytes(payload, "utf-8"))
    res = io.recvline()
    io.recvuntil(b': ')
    return str(res,"utf-8")

io = process('sh')
io.sendline(b'ncat --ssl 158.160.30.225 14000')
io.recvuntil(b': ')
for block in range(4):
    for i in range(16):
        stub = '0'*(15-i)
        target_block = bytes.fromhex(communicate(io,stub))[block*16:(block+1)*16]
        for c in 'abcdefABCDEF0123456789UT{}':
            print(BLUE+'block:'+ENDC, block, BLUE+'pos:'+ENDC, i, BLUE+'testing:'+ENDC, GREEN+flag+YELLOW+c+ENDC)
            cblock = bytes.fromhex(communicate(io,stub+flag+c))[block*16:(block+1)*16]
            print(BLUE+' target_block:'+ENDC, (GREEN if target_block==cblock else RED)+target_block.hex()+ENDC)
            print(BLUE+'current_block:'+ENDC, (GREEN if target_block==cblock else RED)+cblock.hex()+ENDC)
            if cblock == target_block:
                flag += c
                print(BLUE+'flag:'+ENDC,flag)
                break
