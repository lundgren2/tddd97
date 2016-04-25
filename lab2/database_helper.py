#from flask import Flask
import sqlite3
from flask import g
from server import app

# Guide: http://flask.pocoo.org/docs/0.10/patterns/sqlite3/


# Connect to database.db
def connect_db():
    print "connected"
    return sqlite3.connect('database.db')


# Get current database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

# Initializes the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# Teardown active db
def close_db():
    print "close_db"
    get_db().close()

# Getting the cursor, executing and fetching the results
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    get_db().commit() #db.commit
    return (rv[0] if rv else None) if one else rv


# INSERT functions

def signup_user(email, password, firstname, familyname, gender, city, country):
    return query_db('INSERT INTO users VALUES (?,?,?,?,?,?,?)',
            [email, password, firstname, familyname, gender, city, country])


# Login user
def signin_user(email, token):
    return query_db('INSERT INTO loggedInUsers) VALUES (?,?)',
                    [email, token])

def add_message(sender, recipient, message):
    return query_db('INSERT INTO userMessages (sender, recipient, message) VALUES (?,?,?)',
                    [sender, recipient, message])

# GET functions
def get_loggedInUsers(email):
    user = query_db('SELECT * FROM loggedInUsers WHERE email is ?', [email], True)
    if user is None:
        return False
    else:
        return True

def get_user(email):
    return query_db('SELECT * FROM users WHERE email = ?',
        [email], True)
'''
UNNECESSARY
def get_user_by_token(token):
    email = get_email(token)
    return get_user(email)
'''
def get_users():
    return query_db('SELECT * FROM users')

def get_email(token):
    email = query_db('SELECT email FROM loggedInUsers WHERE token IS ?', [token], True)
    if email is not None:
        return email
    else:
        return None

def get_password(email):
    return query_db('SELECT password FROM users WHERE email IS ?', [email], True)

def get_messages(email):
    return query_db('SELECT * FROM userMessages WHERE recipient IS ?', [email], True)

# SET functions
def set_password(email, password):
    return query_db('UPDATE users SET password IS ? AND email IS ?', [password, email])


def valid_login(email, password):
    user = query_db('SELECT * FROM users WHERE email = ? AND password = ?', [email, password], True)
    if user is None:
     return False
    else:
        return True

# Logout user
def signOut(token):
    return query_db('DELETE FROM loggedInUsers WHERE token is ?', [token], True)


