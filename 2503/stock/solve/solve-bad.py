from pwn import *
from server_modified import gen, authorize
from time import sleep

def make5Bytekey(z1,z2,skey):
    res=[]
    for i in range(5):
        if i not in (z1,z2):
            res.append(skey.pop())
        else:
            res.append(0)
    return bytes(res)

def checkbal(io, pubkey):
    io.sendline(bytes('addr '+pubkey, 'utf-8'))
    res = io.recvuntil(b'> ').split(b'\n')
    for line in res:
        if line.startswith(b'balance: '):
            return int(line[9:])

def create_addr():
    return gen(['1234',], verbose=False)

def transfer(io, _from, _to, privkey, balance):
    io.sendline(bytes('pay '+','.join([_from,_to,privkey,str(balance)]), 'utf-8'))
    io.recvuntil(b'> ')
    return checkbal(io,_to)

def get_flag(io, addr, privkey):
    io.sendline(bytes('flag '+','.join([addr,privkey]), 'utf-8'))
    res = io.recvuntil(b'> ')
    return str(res,'utf-8')

io = process('sh')
io.sendline(b'ncat --ssl 158.160.30.225 14001')#(b'ncat --ssl localhost 14001')
io.recvuntil(b'> ')
my_addr = create_addr()
for z1 in range(5):
    for z2 in range(z1+1,5):
        for skey in range(0x1000000):
            try:
                _privkey = (b'\x00'*251+bytes(make5Bytekey(z1,z2,[i for i in skey.to_bytes(3,'big')]))).hex()
            except:
                continue
            _pubkey = gen([_privkey,], verbose=False)
            if authorize(_pubkey, _privkey):
                bal = checkbal(io, _pubkey)
                if bal:
                    my_bal=transfer(io, _pubkey, my_addr, _privkey, bal)
                    print('balance:', my_bal)
                    if my_bal>=35000:
                        print('flag:', get_flag(io, my_addr, '1234'))
                        exit()