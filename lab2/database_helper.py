import sqlite3
from flask import g
from server import app
from contextlib import closing


import os.path
from flask import Flask

#DATABASE = 'database.db'

#db = sqlite3.connect('database.db')
#cursor = db.cursor()


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
def init_db(app):
    with closing(connect_db()) as db:
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("db init done")


# Teardown active db
def close_db():
    print "close_db"
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Getting the cursor, executing and fetching the results
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args) # db.cursor()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# INSERT functions

def signup_user(email, password, firstname, familyname, gender, city, country):
    return query_db('INSERT INTO users (email, password, firstname, familyname, country, city , gender) VALUES (?,?,?,?,?,?,?)',
            [email], [password], [firstname], [familyname], [gender], [city], [country])

def add_message(sender, recipient, message):
    return query_db('INSERT INTO userMessages (sender, recipient, message) VALUES (?,?,?)',
                    [sender], [recipient], [message])

# GET functions
def get_user(email):
    return query_db('SELECT * FROM users WHERE email = ?',
        [email], True)

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
    return query_db('UPDATE users SET password IS ? AND email IS ?', [password], [email])


def valid_login(email, password):
    result = query_db('SELECT * FROM users WHERE email = ? AND password = ?', [email], [password], True)

    if user is None:
     return False
    else:
        return True

# IS USER INLOGGED? (email)
# ADD USER ONLINE?

# Logout user
def signOut(token):
    return query_db('DELETE FROM loggedInUsers WHERE token is ?', [token], True)

# Login user
def add_loggedInUsers(email, token):
    return query_db('INSERT INTO loggedInUsers) VALUES (?,?)',
                    [email], [token])

def get_loggedInUsers(email):
    user = query_db('SELECT * FROM loggedInUsers WHERE email is ?', [email], True)
    if user is None:
        return False
    else:
        return True


'''
def login()
  user = get_user(email)
  if user is None:
      return "Wrong password or mail."
  elif user[email] is email and user[password] is password:

      query_db('INSERT INTO loggedinusers (email, token) VALUES (?,?)',
               (user[email], token)
               )      return True
'''