import random
import base64
data=open('flag.txt.encrypted','rb').read()
encrypted = data[:64]
init_seed=(int(base64.b64decode(data[64:]))//10)*100-100
for seconds in range(200):
    seed = init_seed+seconds
    print('seed:',seed)
    random.seed(seed)
    key=[random.randint(0,255) for i in range(len(encrypted))]
    decrypted = bytes([encrypted[i]^key[i] for i in range(len(encrypted))])
    if decrypted.startswith(b'UCTF{'):
        print(decrypted)
        break
