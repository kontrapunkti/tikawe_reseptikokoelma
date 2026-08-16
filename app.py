from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import config
import recipes, users

import db
db.init_db()

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    recent_recipes = recipes.get_recent_recipes(10)
    return render_template("index.html", recipes=recent_recipes)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = users.get_user_and_pwhash_by_username(username)
    if len(result)==0:
        return render_template("login.html", error=True)
    else:
        user_id = result[0]["id"]
        pw_hash = result[0]["password_hash"]
    if username and check_password_hash(pw_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        return redirect("/user")
    else:
        return render_template("login.html", error=True)

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("registererror.html", error = "Salasanat eivät vastanneet toisiaan")
    if username == "" or password1 == "":
        return render_template("registererror.html", error = "Käyttäjätunnus tai salasana ei voi olla tyhjä merkkijono")
    password_hash = generate_password_hash(password1)
    success = users.create_user(username, password_hash)
    if not success:
        return render_template("register_error.html", error="Käyttäjätunnus on varattu")
    return render_template("login_successful.html")

@app.route("/user")
def user_page():
    if "username" not in session:
        return redirect("/login")
    username = session["username"]
    user_id = session["user_id"]
    user_recipes = recipes.get_user_recipes(user_id)
    return render_template("user.html",username=username,recipes=user_recipes)

@app.route("/new_recipe")
def new_recipe():
    if "username" not in session:
        return redirect("/login")
    return render_template("new_recipe.html")

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect("/login")
    title = request.form["title"]
    content = request.form["content"]
    recipes.create_recipe(session["user_id"], title, content)

    return redirect("/user")

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe_by_id(recipe_id)
    if not recipe:
        return render_template("error.html", error="Reseptiä ei löytynyt")
    return render_template("recipe.html",recipe=recipe)

@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/login")
    recipe = recipes.get_recipe_for_edit(session["user_id"], recipe_id)
    if not recipe:
        return render_template("error.html", error = "Ei käyttöoikeutta tähän reseptiin")
    return render_template("edit_recipe.html",recipe=recipe)

@app.route("/update_recipe/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/login")
    title = request.form["title"]
    content = request.form["content"]
    if not recipes.edit_recipe(session["user_id"], recipe_id, title, content):
        return render_template("error.html", error = "Virhe päivityksessä, ei käyttöoikeutta reseptiin tai muu tekninen virhe. Tarkista kirjautuminen ja kokeile uudestaan.")

    return redirect("/user")

@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/login")

    if not recipes.delete_recipe(session["user_id"], recipe_id):
        return render_template("error.html", error = "Virhe reseptin poistamisessa, ei käyttöoikeutta reseptiin tai muu tekninen virhe. Tarkista kirjautuminen ja kokeile uudestaan.")
    return redirect("/user")

@app.route("/show_user/<int:user_id>")
def show_user(user_id):
    user_recipes = recipes.get_user_recipes(user_id)
    user = users.get_username_from_id(user_id)
    if not user:
        return render_template("Error.html", error = "Käyttäjää ei löytynyt")
    return render_template(
        "show_user.html",
        recipes=user_recipes,
        user=user)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search_results():
    query = request.form["query"]
    result = recipes.search_recipes_from_title(query)
    return render_template("search.html", recipes=result)