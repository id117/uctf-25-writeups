from functools import reduce
from math import gcd

"""
Файл был зашифрован XOR-ом с псевдослучайной последовательностью, содаваемой линейным конгруэнтным генератором (LCG). 
Уязвимость такого метода в том, что зная несколько чисел последовательности, можно восстановить её полностью. 
При этом, нам известно, что зашифрован файл формата png.
"""

##расширенный алгоритм Евклида
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

##деление в модулярной арифметике
def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

##вычисление m
def crack_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    m = abs(reduce(gcd, zeroes))
    return m

##вычисление a
def crack_multiplier(states, m):
    a = (states[2] - states[1]) * modinv(states[1] - states[0], m) % m
    return a


##вычисление c
def crack_increment(states, m, a):
    c = (states[1] - states[0]*a) % m
    return c

##вычисление первых байтов ключа
def get_first_states(path, signature):
    with open(path, 'rb') as src:
        crypted_signature=src.read(len(signature))
    states=tuple(signature[i]^crypted_signature[i] for i in range(len(signature)))
    return states

##вычисление параметров ключа для заданного файла
def crack_png():
    signature = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' #сигнатура файла png - все png начинаются с этих байтов
    path = './flag.png.encrypted'
    states = get_first_states(path, signature)
    m = crack_modulus(states)
    a = crack_multiplier(states, m)
    c = crack_increment(states, m, a)
    print('X[0..'+str(len(states)-1)+'] = '+str(states))
    print('m = '+str(m))
    print('a = '+str(a))
    print('c = '+str(c))
    print('x = '+str(states[0]))
    return a,states[0],c,m, states

def main():
    s=open('flag.png.encrypted','rb')
    e=open('flag.decrypted.png','wb')
    a,x,c,m,_ = crack_png()
    b=s.read(1)
    i=0
    while b:
        e.write((b[0]^x).to_bytes(1,'big'))
        x=(a*x+c)%m
        b=s.read(1)
        i+=1
    e.close()
    print('done')

if __name__=='__main__':
    main()
