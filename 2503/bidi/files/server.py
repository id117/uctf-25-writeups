#!/usr/bin/env python3
from secret import user, password
import random, sys
def auth(n, user, password):
    login = input('? ⁧⁦') #⁩⁦login: ⁩⁩input login
    passwd = input('? ⁧⁦') #⁩⁦pass: ⁩⁩input pass
    print(login, passwd, file=sys.stderr)
    password/=n
    if login == 'admin‮⁦': # check if admin ⁩⁦' and passwd==password*'secret
        print(open('flag.txt').read())
    else:
        print('You are not admin, '+login+'  :(')

auth(random.randint(1,10), user, password)
