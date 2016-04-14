import sqlite3
from flask import g
from contextlib import closing


import os.path
#from flask import Flask

#DATABASE = 'database.db'

db = sqlite3.connect('database.db')
cursor = db.cursor()


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


def before_request():
    g.db = connect_db()


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


# Get user
def get_user(email):
    user = query_db('SELECT * FROM users WHERE email = ?',
        [email], one=True)
    if user is None:
        print 'No such user'
    else:
        return user

# Login user
def signIn(email, password, token):
    user = get_user(email)
    if user is None:
        return "Wrong password or mail."
    elif user[email] is email and user[password] is password:

        query_db('INSERT INTO loggedinusers (email, token) VALUES (?,?)',
                 (user[email], token)
                 )
        return True

# Create user
def signup_contact(email, password, firstname, familyname, gender, city, country):
    query_db('INSERT INTO users (email, password, firstname, familyname, country, city , gender) VALUES (?,?,?,?,?,?,?)',
             (email, password, firstname, familyname, country, city, gender))

#def create_message(email, token)
#def get_token()

