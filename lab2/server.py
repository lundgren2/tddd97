from flask import Flask, request, redirect, url_for, jsonify
import random, re, database_helper # Random token, Regular Expressions (important)

# Create application
app = Flask(__name__)


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


@app.route('/hello/<token>', methods=['GET'])
def hello(token):
    #token = request.form['hej']
    return token


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
            result = database_helper.signup_user(email, password, firstname, familyname, gender, city, country)
            return jsonify(success=True, message="User signed up successfully")

    return jsonify(success=False, message="Formdata are not complete")


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
    email = database_helper.get_email(token)
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
    if database_helper.get_loggedInUsers(email):
        user = database_helper.get_user(email)
    if user is None:
        return jsonify(success=False, message="You are not signed in.")
    else:
        return jsonify(success=True, message="User data retrived.", data=user)


# GET MESSAGE



# Run file as a standalone application
if __name__ == "__main__":
    app.run()
    # app.run(host = '127.0.0.1', port = 5051)
