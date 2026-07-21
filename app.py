from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import config

import db
db.init_db()

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    con = db.connect()
    con.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")
    con.commit()
    result = con.execute("SELECT COUNT(*) FROM visits").fetchone()
    count = result[0]
    recipes = con.execute("SELECT title, content FROM recipes").fetchall()
    con.close()
    return render_template("index.html", visits = count, recipes=recipes)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if len(result)==0:
        return render_template("login.html", error=True)
    else:
        pw_hash = result[0][0]
    if username and check_password_hash(pw_hash, password):
        session["username"] = username
        return render_template("user.html", username=username)
    else:
        return render_template("login.html", error=True)

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/createdemodata")
def createdemodata():
    con = db.connect()
    count = con.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
    if count == 0:
        with open("createdemodata.sql") as f:
            con.executescript(f.read())
    con.commit()
    con.close()

    return redirect("/")

@app.route("/emptytables")
def emptytables():
    db.emptytables()
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    con = db.connect()
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("registererror.html", error = "Salasanat eivät vastanneet toisiaan")
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        con.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("registererror.html", error = "Käyttäjätunnus on jo varattu")
    finally:
        con.commit()
        con.close()

    return "Tunnus luotu"