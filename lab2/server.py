from flask import Flask
from flask import request
import database_helper
import json
#import flask import jsonify

# Create application
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True



# Database connections

@app.before_request
def before_request():
    database_helper.connect_db()

@app.teardown_request
def teardown_request(exception):
    database_helper.close_db()

@app.route("/")
def hello_world():
    return "Hello Worldssa!"


@app.route('/signup', methods=['POST'])
def sign_up():
    request = requset.get_json()
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
def sign_in(email=None, password=None):
    if email != None and password != None:
        result = database_helper.sign_in(email, password)

        if len(result) == 0:
            return 'contact not found', 404
        else:
            return json.dumps(result), 200
    else:
        return "", 404


# Run file as a standalone application
if __name__ == "__main__":
    database_helper.init_db(app)
    app.run()
