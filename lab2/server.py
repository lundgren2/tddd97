import random
import string
import database_helper
from flask import Flask, request, redirect, url_for
from flask import send_from_directory

from flask import Flask
from flask import request
import database_helper
import json
#import flask import jsonify


# Create application
app = Flask(__name__)
app._static_folder = '/Users/tobiaslundgren/GitHub/TDDD97/lab2/static'
app.debug = True


# Database connections

@app.before_request
def before_request():
    database_helper.connect_db()
    database_helper.init_db(app)

@app.teardown_request
def teardown_request(exception):
    database_helper.close_db()

@app.route("/")
def root():
    return app.send_static_file('client.html')

@app.route('/signup', methods=['POST'])
def sign_up():
    request2 = request.get_json()
    email = request2['email']
    password = request2['password']
    firstname = request2['firstname']
    familyname = request2['familyname']
    gender = request2['gender']
    city = request2['city']
    country = request2['country']

    result = database_helper.signup_user(email, password, firstname, familyname, gender, city, country)
    if result is True:
        return 'Successfully created a new user.', 200
    else:
        return 'Form data missing or incorrect type.', 501


@app.route('/login/<email>/<password>', methods=['GET'])
def signIn(email=None, password=None):

    # Create token
    token = ''.join(random.choice(string.lowercase) for i in range(35))

    print token
    if email != None and password != None:
        result = database_helper.signIn(email, password, token)

        if result != True:
            return 'user not found or wrong password', 404
        else:
            return token
    else:
        return "", 404



# @app.route('/get_message/<email>/<password>', methods=['GET'])

# Run file as a standalone application
if __name__ == "__main__":
#    database_helper.init_db(app)
    app.run()
    #app.run(host = '127.0.0.1', port = 5051)
