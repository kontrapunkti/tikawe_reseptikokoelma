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

    return """Tunnus luotu <p><a href="/login">Kirjaudu sisään</a></p>"""

@app.route("/user")
def user_page():
    if "username" not in session:
        return redirect("/login")
    
    username = session["username"]      

    sql = """
    SELECT recipes.id, recipes.title
    FROM recipes, users
    WHERE recipes.creator_id = users.id
    AND users.username = ?
    """

    recipes = db.query(sql, [username])
    
    return render_template("user.html",username=username,recipes=recipes)

@app.route("/new_recipe")
def new_recipe():
    if "username" not in session:
        return redirect("/login")
    
    return render_template("new_recipe.html")

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    title = request.form["title"]
    content = request.form["content"]

    user = db.query("SELECT id FROM users WHERE username = ?",[username])
    user_id = user[0]["id"]

    con = db.connect()
    con.execute(
        "INSERT INTO recipes (creator_id, title, content) VALUES (?, ?, ?)",
        [user_id, title, content]
    )
    con.commit()
    con.close()

    return redirect("/user")