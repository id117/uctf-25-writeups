import random, time, sys
def create_sbox():
    hex = '0123456789abcdef'
    sbox = list('▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐')
    random.shuffle(sbox)
    return {hex[i]:sbox[i] for i in range(16)}

def sbox(box, char):
    return box[char]

def encrypt(box, hex):
    return ''.join([sbox(box,c) for c in hex])

def main():
    box = create_sbox()
    lastbox = time.time()
    print('encrypted flag:', encrypt(box, bytes(open('flag.txt').read().strip('\n'),'utf-8').hex()))
    while 1:
        inp = input('> ')
        print(inp, file=sys.stderr)
        try:
            bytes.fromhex(inp.lower())
        except:
            print('input must be hex-encoded!')
            continue        
        if time.time()-lastbox > 5:
            box = create_sbox()
            lastbox = time.time()
            print('update: encryption keys have changed just now')
            print('encrypted flag:', encrypt(box, open('flag.txt','rb').read().hex()))
        print('',encrypt(box, inp))
main()
