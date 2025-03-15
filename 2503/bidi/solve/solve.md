xxd server.py:
```
00000000: 2321 2f75 7372 2f62 696e 2f65 6e76 2070  #!/usr/bin/env p
00000010: 7974 686f 6e33 0a66 726f 6d20 7365 6372  ython3.from secr
00000020: 6574 2069 6d70 6f72 7420 7573 6572 2c20  et import user, 
00000030: 7061 7373 776f 7264 0a69 6d70 6f72 7420  password.import 
00000040: 7261 6e64 6f6d 2c20 7379 730a 6465 6620  random, sys.def 
00000050: 6175 7468 286e 2c20 7573 6572 2c20 7061  auth(n, user, pa
00000060: 7373 776f 7264 293a 0a20 2020 206c 6f67  ssword):.    log
00000070: 696e 203d 2069 6e70 7574 2827 3f20 e281  in = input('? ..
00000080: a7e2 81a6 2729 2023 e281 a9e2 81a6 6c6f  ....') #......lo
00000090: 6769 6e3a 20e2 81a9 e281 a969 6e70 7574  gin: ......input
000000a0: 206c 6f67 696e 0a20 2020 2070 6173 7377   login.    passw
000000b0: 6420 3d20 696e 7075 7428 273f 20e2 81a7  d = input('? ...
000000c0: e281 a627 2920 23e2 81a9 e281 a670 6173  ...') #......pas
000000d0: 733a 20e2 81a9 e281 a969 6e70 7574 2070  s: ......input p
000000e0: 6173 730a 2020 2020 7072 696e 7428 6c6f  ass.    print(lo
000000f0: 6769 6e2c 2070 6173 7377 642c 2066 696c  gin, passwd, fil
00000100: 653d 7379 732e 7374 6465 7272 290a 2020  e=sys.stderr).  
00000110: 2020 7061 7373 776f 7264 2f3d 6e0a 2020    password/=n.  
00000120: 2020 6966 206c 6f67 696e 203d 3d20 2761    if login == 'a
00000130: 646d 696e e280 aee2 81a6 273a 2023 2063  dmin......': # c
00000140: 6865 636b 2069 6620 6164 6d69 6e20 e281  heck if admin ..
00000150: a9e2 81a6 2720 616e 6420 7061 7373 7764  ....' and passwd
00000160: 3d3d 7061 7373 776f 7264 2a27 7365 6372  ==password*'secr
00000170: 6574 0a20 2020 2020 2020 2070 7269 6e74  et.        print
00000180: 286f 7065 6e28 2766 6c61 672e 7478 7427  (open('flag.txt'
00000190: 292e 7265 6164 2829 290a 2020 2020 656c  ).read()).    el
000001a0: 7365 3a0a 2020 2020 2020 2020 7072 696e  se:.        prin
000001b0: 7428 2759 6f75 2061 7265 206e 6f74 2061  t('You are not a
000001c0: 646d 696e 2c20 272b 6c6f 6769 6e2b 2720  dmin, '+login+' 
000001d0: 203a 2827 290a 0a61 7574 6828 7261 6e64   :(')..auth(rand
000001e0: 6f6d 2e72 616e 6469 6e74 2831 2c31 3029  om.randint(1,10)
000001f0: 2c20 7573 6572 2c20 7061 7373 776f 7264  , user, password
00000200: 290a                                     ).
```

Здесь использованы bidi-символы юникода для изменения направления текста.

Из-за этого, вот такой код:
```
#!/usr/bin/env python3
from secret import user, password
import random
def auth(n):
    login = input('? <RLI><LRI>') #<PDI><LRI>login: <PDI><PDI>input login
    passwd = input('? <RLI><LRI>') #<PDI><LRI>pass: <PDI><PDI>input pass
    password/=n
    if login != 'admin<RLO><LRI>': # check if admin <PDI><LRI>' and passwd==password*'secret
        print(open('flag.txt').read())
    else:
        print('You are not admin, '+login+'  :(')

auth(random.randint(1,10))
```

выглядит вот так:
```
#!/usr/bin/env python3
from secret import user, password
import random, sys
def auth(n, user, password):
    login = input('? login: ') #input login
    passwd = input('? pass: ') #input pass
    print(login, passwd, file=sys.stderr)
    password/=n
    if login == 'admin' and passwd==password*'secret': #check if admin
        print(open('flag.txt').read())
    else:
        print('You are not admin, '+login+'  :(')

auth(random.randint(1,10), user, password)
```

Соответственно, чтобы получить флаг, нужно, чтобы login был 'admin\[U+202E\]\[U+2066\]'.

Подробнее: https://en.wikipedia.org/wiki/Trojan_Source