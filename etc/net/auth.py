from .db import db_con
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import et.etc.security.cxi as cxi

def auth(username, password=None, id_=None):
    conn = db_con()
    if '@' and '.' in username:
        if password == None and id_ == None:
            query = cxi.encrypt((f"SELECT email, password FROM `users` WHERE email='{username}'"))
        else:
            query = cxi.encrypt((f"SELECT email, password FROM `users` WHERE AND email='{username}' AND password='{password}'"))
    else:
        uname = username.split()
        fname = uname[0]
        lname = uname[1]
        if password == None and id_ == None:
            query = cxi.encrypt((f"SELECT email, password FROM `users` WHERE firstname='{fname}' AND lastname='{lname}'"))
        else:
            query = cxi.encrypt((f"SELECT id, email, password FROM `users` WHERE firstname='{fname}' AND lastname='{lname}' AND password='{password}'"))
    try:
        result = conn.execute(cxi.decrypt(query)).fetchall()
        if result[0] == '':
            return False
        else:
            return True
    except:
        return False
    conn.close()
