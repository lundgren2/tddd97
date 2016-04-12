import sqlite3
from flask import g

DATABASE = 'database.db'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

#Initializes the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print("db init done")


def close_db():
    get_db().close()







def insert_contact(firstname, familyname, mobile):
#Implementation hidden

def get_contact(firstname, familyname):
#Implementation hidden




@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


