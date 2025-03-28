import socket
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import et.etc.security.cxi as cxi

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"

def _auth(conn, username, password=None, id_=None):
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

def _signup(conn, id_, username, password, email, gender, date=None, profile='default.jpg', c20='ucf'):
    try:
        uname = username.split()
        fname = uname[0]
        lname = uname[1]
        conn.execute(
        	"INSERT INTO user (id, firstname, lastname, password, email, gender, profile, c20)"
        	" VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        	(id_, fname, lname, password, email, gender, profile, c20))
        conn.commit()
        return True
    except:
        return False
    return False
    
class Proxy(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.wsgi_app = ReverseProxied(self.app.wsgi_app)

        return self


class ReverseProxied(object):
    """
    Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:

    location /prefix {
        proxy_pass http://192.168.43.2:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /prefix;
        }

    :param app: the WSGI application
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ.get('PATH_INFO', '')
            if path_info and path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        server = environ.get('HTTP_X_FORWARDED_SERVER_CUSTOM', 
                             environ.get('HTTP_X_FORWARDED_SERVER', ''))
        if server:
            environ['HTTP_HOST'] = server

        scheme = environ.get('HTTP_X_SCHEME', '')

        if scheme:
            environ['wsgi.url_scheme'] = scheme

        return self.app(environ, start_response)

def signup(conn, session, id_, username, password, email, gender):
    try:
        if fname and lname and id_ and password and email:
            username = fname + ' ' + lname
            try:
                if _signup(conn, id_, username, password, email, gender) == True:
                    os.mkdir('et/uploads/users/{}'.format(id_))
                    session.permanent = True
                    session['loggedin'] = True
                    session['username'] = cxi.encrypt(username)
                    session['id'] = id_
                    return True
                else:
                    False
            except:
                return None
    except:
        return False
        
