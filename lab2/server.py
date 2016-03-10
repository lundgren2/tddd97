from flask import app, request
from flask import Flask
import database_helper
import json



#Lesson 2

app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
    database_helper.connect_db()

@app.teardownrequest
def teardown_request(exception):
    database_helper.close_db()


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route('/signup', methods=['POST'])
def signup():

    email = request.get_json()['email']
    password = request.get_json()['password']
    firstname = request.get_json()['firstname']
    familyname = request.get_json()['familyname']
    gender = request.get_json()['gender']
    city = request.get_json()['city']
    country = request.get_json()['country']
    #messages = ???

result = database_helper.signup_contact(email, password, firstname, familyname, gender, city, country)
    if result == True:
        return 'Successfully created a new user.', 200
    else:
        return 'Form data missing or incorrect type.', 501



@app.route('/sign_in/<email>/<password>', methods=['GET'])
def login(email, password):

   # result = database_helper.get_contact(email, password)
    email = request.form['email']
    password = request.form['password']


if __name__ == "__main__":
    app.run()
