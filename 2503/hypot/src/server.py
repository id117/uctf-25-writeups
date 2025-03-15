import random, sys
def func(a,b):
  inp = input('? ')[:11][::-1]
  print(inp, file=sys.stderr)
  return eval(inp)
a=random.randint(1,100000)
b=random.randint(1,100000)
if func(a,b)==(a**2+b**2)**0.5:
  print(open('flag.txt').read())
