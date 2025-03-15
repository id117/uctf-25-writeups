import random
import time
import os
data=open('flag.txt','rb').read()
assert(len(data)==64)
seed = int(time.time()*10)
random.seed(seed)
print(seed)
key=[random.randint(0,255) for i in range(len(data))]
open('flag.txt.encrypted','wb').write(bytes([data[i]^key[i] for i in range(64)]))
print('done')
os.system('stat -c "%Y" flag.txt.encrypted|base64 >> flag.txt.encrypted')
