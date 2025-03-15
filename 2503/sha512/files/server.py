import random, os, sys, hashlib

while True:
    inp = input('> ')
    print(inp, file=sys.stderr)
    os.system('bash -c "echo {} >> log.txt" 1>/dev/null 2>/dev/null'.format(inp))
    hash = hashlib.sha512(bytes(inp, 'utf-8')).digest()
    if hash == bytes(random.randint(0,255) for i in range(64)):
        print(open('flag.txt').read())