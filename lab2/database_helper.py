import os
import sqlite3 #V
from flask import g #V

DATABASE = 'database.db' # V


# Connect to database.db
def connect_db():
    return sqlite3.connect(app.config['DATABASE']) # V


# Get current database connection
def get_db():
    db = getattr(g, '_database', None) #g? #V
    if db is None:
        db = g._database = connect_to_database()
    return db

# Initializes the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print("db init done")


@app.before_request
def before_request():
    g.db = connect_db()


# Teardown active db
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Getting the cursor, executing and fetching the results
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# Get user
def get_user(email):
    user = query_db('select * from users where email = ?', 
        [email], one=True)
    if user is None:
    print 'No such user'
else:
    return userData







@app.teardown_appcontext
def close_connection(exception): #Argument db?
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


