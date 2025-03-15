import base58
from secrand import secrand
from Crypto.Hash import keccak
import json
import time
import random
from asciichartpy import plot
import cmd
import sys

def init():
    return json.loads(open('db.json').read())

db = init()

price = [random.randint(25000,35000) for i in range(75)]

def validate(addr):
    if not(addr.startswith('1337x')):
        print('Invalid address: "'+addr+'"')
        return False
    try:
        if len(base58.b58decode(addr[5:]))==32:
            return True
        else:
            print('Invalid address: ', addr)
            return False
    except:
        print('Invalid address: ', addr)
        return False

def authorize(addr, privkey):
    try:
        assert(validate(addr))
        assert(gen([privkey,], verbose= False)==addr)
        return True
    except:
        print('Error unauthorized (wrong privkey)')
        return False

helpmsg = '''available commands:
help                            -- print this text
top N,OFFSET                    -- top rich addresses
                                    (N<=1000, from OFFSET place)
gen PRIVKEY                     -- generate address with
                                    your privkey (hex format)
addr ADDR                       -- show address info 
                                    (balance and 
                                    transaction history)
tr TID                          -- show transaction info
trs N,OFFSET                    -- show last N transactions
                                    (N<=1000, from OFFSET 
                                    transaction)
pay ADDR1,ADDR2,PRIVKEY,AMOUNT  -- transfer
                                    AMOUNT coins 
                                    from ADDR1 to ADDR2
                                    (PRIVKEY required)
stock                           -- show stock chart
flag ADDR,PRIVKEY               -- buy flag using 
                                    ADDR balance
                                    (PRIVKEY required)
history                         -- show command history
exit'''

def help(args):
    print(helpmsg)

def gen(args, verbose = True):
    if len(args) < 1:
        print('invalid args')
        return
    try:
        privkey = bytes.fromhex(args[0])
    except:
        print('invalid privkey, must be hexencoded')
        return
    k = keccak.new(digest_bits=256)
    k.update(privkey)
    pubkey = '1337x'+str(base58.b58encode(k.digest()),'UTF-8')
    if verbose: print(pubkey)
    return pubkey

def top(args):
    if len(args) < 2:
        print('invalid args')
        return
    try:
        n = int(args[0])
        offset = int(args[1])
    except:
        print('invalid args')
        return
    if n>=1000:
        n = 1000
    try:
        res = sorted(db['ads'].items(), key=lambda item: item[1], reverse=True)[offset:offset+n]
    except:
        print('error')
        return
    for i in res:
        print('addr:', i[0], 'bal:', i[1])
    return

def addr(args):
    if len(args) < 1:
        print('invalid args')
        return
    addr = args[0]
    if not(validate(addr)):
        return
    print('address:', addr)
    if addr not in db['ads'].keys():
        print('balance:', 0)
        return
    print('balance:', db['ads'][addr])
    print('outgoing transactions: ')
    for tid in range(len(db['trs'])):
        tr = db['trs'][tid]
        if tr['from'] == addr:
            print('tid_'+str(tid))
    print('incoming transactions: ')
    for tid in range(len(db['trs'])):
        tr = db['trs'][tid]
        if tr['to'] == addr:
            print('tid_'+str(tid))
    return

def tr(args):
    if len(args) < 1:
        print('invalid args')
        return
    tid = args[0]
    if not(tid.startswith('tid_')):
        print("Invalid tid: ", tid)
        return
    try:
        tid = int(tid[4:], 10)
        tr = db['trs'][tid]
    except:
        print("Transaction", tid, "not exist")
        return
    print('id: tid_'+str(tid))
    print('from:',tr['from'])
    print('to:',tr['to'])
    print('amount:',tr['amount'])
    print('timestamp:',tr['timestamp'])

def trs(args):
    try:
        n = int(args[0])
        offset = int(args[1])
        assert(n>0)
        assert(offset>=0)
        if n>=1000: n=1000
        assert(n+offset<len(db['trs']))
        assert(offset<len(db['trs']))
        for i in range(len(db['trs'])-offset-n,len(db['trs'])-offset,1):
            print('tid_'+str(i))
    except:
        print('error')
        return
    return

def pay(args):
    try:
        print('pay')
        _from, _to, privkey, amount = args
        amount = int(amount)
        assert(validate(_from))
        assert(validate(_to))
        assert(db['ads'][_from] >= amount)
        assert(authorize(_from,privkey))
        db["trs"].append(
            {
                "from":_from,
                "to":_to,
                "amount":amount,
                'timestamp':time.time()
            }
        )
        if _to not in db["ads"].keys():
            db['ads'][_to]=0
        db['ads'][_from]-=amount
        db['ads'][_to]+=amount
        tid = "tid_"+str(len(db["trs"])-1)
        print(tid)
        return
    except:
        print('error')
        return

def stock(args):
    print(plot(price[-75:],{'height':10,'format':'{:8.0f}'}))

def flag(args):
    try:
        addr, privkey = args
        assert(authorize(addr,privkey))
        assert(db['ads'][addr] >= price[-1])
        db["trs"].append(
            {
                "from":addr,
                "to":"flag",
                "amount":price[-1],
                'timestamp':time.time()
            }
        )
        db['ads'][addr]-=price[-1]
        print(open('flag.txt').read())
    except:
        print('error')
        return

commands = []
class CmdParse(cmd.Cmd):
    prompt = "> "
    def do_help(self, arg):
        help([])
    def do_listall(self):
        for i, command in enumerate(commands):
            print(i, command)
    def default(self, line):
        print(line, file=sys.stderr)
        commands.append(line)
        inp = line.strip(' ').split(' ')
        cmd = inp[0]
        if len(inp)>1:
            args = inp[1].split(',')
        else:
            args = []
        exec_cmd(cmd, args)
cli = CmdParse()

def history(args):
    cli.do_listall()

allowed_commands = {
    'help':help,
    'top':top,
    'gen':gen,
    'addr':addr,
    'tr':tr,
    'trs':trs,
    'pay':pay,
    'stock':stock,
    'flag':flag,
    'history':history,
    'exit':exit
}

def exec_cmd(cmd, args):
    price.append(random.randint(25000,35000))
    if (cmd not in allowed_commands.keys()):
        return
    allowed_commands[cmd](args)
    
def main():
    print('Welcome!')
    help(1)
    cli.cmdloop()

if __name__ == "__main__":
    main()
