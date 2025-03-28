import sqlite3
from flask import g
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def db_con():
    if "db" not in g:
        g.db = sqlite3.connect("db/db1.db")
        g.db.row_factory = sqlite3.Row
    return g.db

def msgs_db_con():
    if "msgdb" not in g:
        g.msgdb = sqlite3.connect("db/db2.db")
        g.msgdb.row_factory = sqlite3.Row
    return g.msgdb

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

