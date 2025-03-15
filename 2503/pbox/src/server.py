import random, time, sys
def create_pbox():
    size = random.randint(5,128)
    pbox = [i for i in range(size)]
    random.shuffle(pbox)
    return size, pbox

def pbox(buf, box):
    return ''.join([buf[i] for i in box])

def encrypt(buf, box, size):
    return ''.join([pbox(buf[i:i+size],box) for i in range(0,len(buf),size)])

def pad(buf, size):
    res = buf
    for i in range(size):
        if (len(res)%size==0) and (size<=len(res)):
            return res
        elif len(res)==0:
            return buf
        res += '.'

def main():
    size, box = create_pbox()
    print('box size:', size)
    lastbox = time.time()
    print('encrypted flag:', encrypt(pad(open('flag.txt').read().strip('\n'), size), box, size))
    while 1:
        if time.time()-lastbox > 5:
            size, box = create_pbox()
            lastbox = time.time()
            print('update: encryption keys have changed just now')
            print('box size:', size)
            print('encrypted flag:', encrypt(pad(open('flag.txt').read().strip('\n'), size), box, size))
        inp = pad(''+input('> '), size)
        print(inp, file=sys.stderr)
        print(encrypt(inp, box, size))
main()
