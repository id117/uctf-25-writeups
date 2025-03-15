import json, sys, sqlite3, os

os.system('cp bank.db tmp.db')

help = '''
Payments will be available from June 2025, but you can register now.
Available commands:
{"cmd":"reg", "user":"<string>", "password":"<string>"}
{"cmd":"login", "user":"<string>", "password":"<string>"}
{"cmd":"exit"}
'''

def reg(data):
    try:
        assert(data['cmd']=='reg')
        assert(data['user']!='')
        session['crs'].execute("select name from user".format(data['user']))
        assert(data['user'] not in [i[0] for i in session['crs'].fetchall()])
        assert(data['password']!='')
        session['crs'].execute("insert into user values ('{}','{}')".format(data['user'], data['password']))
        session['conn'].commit()
    except:
        print('reg error')
    return

def login(data):
    try:
        assert(data['cmd']=='login')
        assert(data['user']!='')
        session['crs'].execute("select name,password from user".format(data['user'], data['password']))
        assert((data['user'],data['password']) in [(i[0],i[1]) for i in session['crs'].fetchall()])
        session['logged_in'] = True
        session['username'] = data['user']
    except:
        print('login error')
    return


def flag(data):
    try:
        assert(data['cmd']=='flag')
        assert(session['username']=='admin')
        print(open('flag.txt').read())
    except:
        print('flag error')
    return

allowed_cmds = {
    "reg":reg,
    "login":login,
    "flag":flag,
    "exit":exit
}

def execute_cmd(data):
    return allowed_cmds[data['cmd']](data)

conn = sqlite3.connect('tmp.db')
crs = conn.cursor()
session={'conn':conn, 'crs':crs}

def main():
    print(help)
    cmd = ''
    while cmd != 'exit':
        try:
            inp = input('jsonbank> ')
            print(inp, file=sys.stderr)
            data = json.loads(inp)
            assert(data['cmd'] in allowed_cmds)
        except:
            print('invalid json')
            continue
        execute_cmd(data)

main()