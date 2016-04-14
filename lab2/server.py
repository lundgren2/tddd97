import random
import string
import database_helper

from flask import app
from flask import Flask, request, redirect, url_for, send_from_directory


# Create application
app = Flask(__name__)
#app.config.from_object(__name__)
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
    request = request.get_json()
    email = request['email']
    password = request['password']
    firstname = request['firstname']
    familyname = request['familyname']
    gender = request['gender']
    city = request['city']
    country = request['country']
    # messages = ???

    result = database_helper.signup_contact(email, password, firstname, familyname, gender, city, country)
    if result is True:
        return 'Successfully created a new user.', 200
    else:
        return 'Form data missing or incorrect type.', 501


@app.route('/login/<email>/<password>', methods=['GET'])
def signIn(email=None, password=None):
    token = ''.join(random.choice(string.lowercase) for i in range(32))

    print token
    if email != None and password != None:
        result = database_helper.signIn(email, password, token)

        if result != True:
            return 'user not found or wrong password', 404
        else:
            return token
    else:
        return "", 404

#@app.route('/get_message/<email>/<password>', methods=['GET'])

# Run file as a standalone application
if __name__ == "__main__":
    app.run()
