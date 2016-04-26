from flask import Flask, request, redirect, url_for, jsonify
import random, re, string, database_helper, json # Random token, Regular Expressions (important)

# Create application
app = Flask(__name__)
app.debug = True

# Database connections
@app.before_request
def before_request():
    database_helper.connect_db()

@app.teardown_request
def teardown_request(exception):
    database_helper.close_db()


@app.route("/")
def root():
    return redirect('static/client.html')


@app.route('/signin2', methods=['POST'])
def signIn2():
    email = request.form['email']
    password = request.form['password']
    # Check valid user
    if database_helper.valid_login(email, password):
    #if result is False:
        return jsonify(success=False, message="Wrong password or email")
    else:
        return "YOLO"


@app.route('/helloz', methods=['POST'])
def helloz():
    token = request.form['token']
    return token

@app.route('/signup', methods=['POST'])
def signUp():
    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    familyname = request.form['familyname']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']

    if len(email) != 0 and len(firstname) != 0 and len(familyname) != 0 and len(gender) != 0 and len(city) != 0 and \
    len(country) != 0:
        print "form exist"
        if len(password) < 7:
            return jsonify(success=False, message="Password is too short")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify(success=False, message="Email is invalid")
        if database_helper.get_user(email):
            return jsonify(success=False, message="Email already exists")
        else:
            database_helper.signup_user(email, password, firstname, familyname, gender, city, country)
            return jsonify(success=True, message="User signed up successfully")

    return jsonify(success=False, message="Formdata are not complete")


@app.route('/signin', methods=['POST'])
def signIn():
    email = request.form['email']
    password = request.form['password']
    # Check valid user
    if database_helper.valid_login(email, password):
        if database_helper.get_loggedInUsers(email):
            return jsonify(success=False, message="Already signed in")
        # Create token
        token = ''.join(random.choice(string.lowercase) for i in range(35))
        print token
        user = database_helper.signin_user(email, token)
        if user is not None:
            return jsonify(success=True, message="User successfully signed in")
    else:
        return jsonify(success=False, message="Wrong password or email")


@app.route('/signout', methods=['POST'])
def signOut():
    token = request.form['token']
    if token:
        database_helper.signOut(token)
        return jsonify(sucess=True, message="User signed out successfully")
    else:
        return jsonify(sucess=False, message="No token!")


@app.route('/changepass', methods=['POST'])
def changePass():
    token = request.form['token']
    old_Password = request.form['old_password']
    new_Password = request.form['new_password']
    email = database_helper.get_email(token)
    email = email[0]

    print email
    curr_pw = database_helper.get_password(email)
    curr_pw = curr_pw[0]
    print curr_pw

    if len(new_Password) < 7:
        return jsonify(success=False, message="Too short password")

    if not email:
        return jsonify(success=False, message="Invalid token")

    if curr_pw == old_Password:
        database_helper.set_password(email, new_Password)
        return jsonify(sucess=True, message="Password changed successfully")
    else:
        return jsonify(sucess=False, message="Wrong password")

@app.route('/getuserdatabytoken', methods=['POST'])
def getUserDataByToken():
    token = request.form['token']
    email = database_helper.get_email(token)
    email = email[0]
    if database_helper.get_loggedInUsers(email):
        user = database_helper.get_user(email)
    if user is None:
        return jsonify(success=False, message="User not signed in!")
    else:
        return jsonify(success=True, message="User data retrieved.", data=user)


@app.route('/getuserdatabyemail', methods=['POST'])
def getUserDataByEmail():
    token = request.form['token']
    email = request.form['email']
    checkuser = database_helper.get_email(token)
    checklogin = database_helper.get_loggedInUsers(checkuser[0])
    if checklogin:
        user = database_helper.get_user(email)
        if not user:
            return jsonify(success=False, message="User not signed in!")
        else:
            return jsonify(success=True, message="User data retrieved.", data=user)


# GET MESSAGE
@app.route('/getusermessagebytoken', methods=['POST'])
def getUserMessageByToken():
    token = request.form['token']
    email = database_helper.get_email(token)
    email = email[0]
    if not email:
        return jsonify(success=False, message="Error!")
    else:
        messages = database_helper.get_messages(email)
        if not messages:
            return jsonify(success=True, message="No messages for user")
        else:
            return jsonify(success=True, message="User messages retrieved.", data=messages)


@app.route('/getusermessagebyemail', methods=['POST'])
def getUserMessageByEmail():
    token = request.form['token']
    email = request.form['email']
    if checkLogin(token):
        user = database_helper.get_messages(email)
        if not user:
            return jsonify(success=True, message="No messages for user")
        else:
            return jsonify(success=True, message="User data retrieved.", data=user)


@app.route('/postmessage', methods=['POST'])
def postMessage():
    token = request.form['token']
    message = request.form['message']
    recepient = request.form['email']
    sender = database_helper.get_email(token)
    sender = sender[0]

    if checkLogin(token):
        database_helper.add_message(sender, recepient, message)
        return jsonify(success=True, message="Message sent")


def checkLogin(token):
    email = database_helper.get_email(token)
    email = email[0]
    result = database_helper.get_loggedInUsers(email)
    if not result:
        return False
    else:
        return True


# Run file as a standalone application
if __name__ == "__main__":
    app.run()
    # app.run(host = '127.0.0.1', port = 5051)
