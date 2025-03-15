import os, random
def secrand(size):
    twister = [i for i in os.urandom(3 if size > 3 else size)]
    if size>4:
        twister = [0 for i in range(min(size, 5)-len(twister))]+twister
    random.shuffle(twister)
    twister = [0 for i in range(size-len(twister) if size> 5 else 0)] + twister
    return bytes(twister)