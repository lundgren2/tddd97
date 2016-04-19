import random
import string
import re
import database_helper
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from flask import Flask
from flask import request
import database_helper
# import json
from flask import jsonify

# Create application
app = Flask(__name__)
app._static_folder = '/Users/tobiaslundgren/GitHub/TDDD97/lab2/static'
app.debug = True

# Session
socket = {}


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
def signUp():
    getjson = request.get_json()
    email = getjson['email']
    password = getjson['password']
    firstname = getjson['firstname']
    familyname = getjson['familyname']
    gender = getjson['gender']
    city = getjson['city']
    country = getjson['country']

    if len(email) != 0 and len(firstname) != 0 and len(familyname) != 0 and len(gender) != 0 and len(city) != 0 and len(
            country) != 0:
        if len(password) < 7:
            return jsonify(success=False, message="Password is too short")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify(success=False, message="Email is invalid")
        result = database_helper.signup_user(email, password, firstname, familyname, gender, city, country)
        if result is None:
            return jsonify(success=False, message="Email already exists")
        else:
            return jsonify(success=True, message="User signed up successfully")
    return jsonify(success=True, message="Formdata are not complete")


@app.route('/signin', methods=['POST'])
def signIn():
    getjson = request.get_json()
    email = getjson['email']
    password = getjson['password']
    # Check valid user
    result = database_helper.valid_login(email, password)
    if result is None:
        return jsonify(success=False, message="Wrong password or email")
    else:
        # Create token
        token = ''.join(random.choice(string.lowercase) for i in range(35))
        print token
        result = database_helper.signin_user(email, token)
        if result:
            return jsonify(success=True, message="User successfully signed in")


@app.route('/signout', methods=['POST'])
def signOut():
    token = request.form['token']
    if database_helper.signOut(token):
        return jsonify(sucess=True, message="User signed out successfully")
    else:
        return False


@app.route('/changepass', methods=['POST'])
def changePass():
    getjson = request.get_json()
    token = getjson['token']
    old_Password = getjson['old_password']
    new_Password = getjson['new_password']
    email = database_helper.get_email(token)

    if len(new_Password) < 7:
        return jsonify(success=False, message="Too short password")

    if email is None:
        return jsonify(success=False, message="Invalid token")

    if database_helper.get_password(email) == old_Password:
        database_helper.set_password(email, new_Password)
        return jsonify(sucess=True, message="Password changed successfully")

@app.route('/getuserdatabytoken', methods=['POST'])
def getUserDataByToken():
    token = request.form['token']
    user = database_helper.get_user_by_token(token)
    if user is None:
        return jsonify(success=False, message="Invalid token")
    user = database_helper.get_user(email)
    if user is None:
        return jsonify(success=False, message="User doesn't exist")
    else:
        return jsonify(success=True, message="User data retrieved.", data=user)


#MÅSTE FIXAS
@app.route('/getuserdatabyemail', methods=['POST'])
def getUserDataByEmail():
    token = request.form['token']
    token = request.form['email']
    if database_helper.get_loggedInUsers(email)
    email = database_helper.get_email(token)

    user = database_helper.get_user(email)


getUserDataByToken: function(token)
{
    var
email = tokenToEmail(token);
return serverstub.getUserDataByEmail(token, email);
},

getUserDataByEmail: function(token, email)
{
if (loggedInUsers[token] != null){
if (users[email] != null) {
var match = copyUser(users[email]);
delete match.messages;
delete match.password;
return {"success": true, "message": "User data retrieved.", "data": match};
} else {
return {"success": false, "message": "No such user."};
}
} else {
return {"success": false, "message": "You are not signed in."};
}
},



#@app.route('/get_message/<email>/<password>', methods=['GET'])

# Run file as a standalone application
if __name__ == "__main__":
    #    database_helper.init_db(app)
    app.run()
    # app.run(host = '127.0.0.1', port = 5051)
