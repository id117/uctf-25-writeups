from secret import a,x,c,m
s=open('flag.png','rb')
e=open('flag.png.encrypted','wb')
b=s.read(1)
i=0
while b:
    e.write((b[0]^x).to_bytes(1,'big'))
    x=(a*x+c)%m
    b=s.read(1)
    i+=1
e.close()
print('done')
    
