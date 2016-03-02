from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/sign_in/<email>/<password>")
def login(email,password):

    email = request.form['email']
    password = request.form['password']


if __name__ == "__main__":
    app.run()
