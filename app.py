from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    if username:
        return render_template("user.html", username=username)
    else:
        return render_template("login.html", error=True)

@app.route("/login")
def login_page():
    return render_template("login.html")