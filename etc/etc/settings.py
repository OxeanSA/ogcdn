import os
from os import environ, path
import socket

class settings:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def _rev(ip="127.0.0.1", switch=False):
        if switch == True:
            pass
          # prior = prior("lookup", False, ip, "ipv4")
          # if prior == True:
              # pass
                # Code unfinished!
    def _getip(lookup='local'):
        if lookup == 'local':
            ip = None
            
class Config:
    environ['SECRET_KEY'] = '$x2&yzbhbvesoy3)g@dx!d=iv2+86ugr5'
    environ['SESSION_COOKIE_NAME'] = 'crtooui'
    environ['STATIC_FOLDER'] = 'et/'
    environ['TEMPLATES_FOLDER'] = './'
    environ['DATABASE_URI'] = 'db/db1.db'
class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')
class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get['DATABASE_URI']