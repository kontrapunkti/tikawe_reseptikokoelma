import secrets
from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import recipes
import users
import ratings

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    recent_recipes = recipes.get_recent_recipes(10)
    return render_template("index.html", recipes=recent_recipes)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    if len(username) > 50 or len(password) > 50:
        return render_template("error.html",
                               error="Liian pitkä käyttäjätunnus tai salasana")
    if not username or not password:
        return render_template("login.html", error=True)
    result = users.get_user_and_pwhash_by_username(username)
    if len(result)==0:
        return render_template("login.html", error=True)
    user_id = result[0]["id"]
    pw_hash = result[0]["password_hash"]
    if username and check_password_hash(pw_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/user")
    return render_template("login.html", error=True)

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"].strip()
    password1 = request.form["password1"].strip()
    password2 = request.form["password2"].strip()
    if len(username) > 50 or len(password1) > 50 or len(password2) > 50:
        return render_template("error.html",
                               error="Liian pitkä käyttäjätunnus tai salasana")
    if not username or not password1 or not password2:
        return render_template("register.html",
                               error = """Käyttäjätunnus tai
                               salasana ei voi olla tyhjä merkkijono""")
    if password1 != password2:
        return render_template("register.html",
                               error = "Salasanat eivät vastanneet toisiaan")
    if username == "" or password1 == "":
        return render_template("register.html",
                               error = """Käyttäjätunnus tai salasana
                               ei voi olla tyhjä merkkijono""")
    password_hash = generate_password_hash(password1)
    success = users.create_user(username, password_hash)
    if not success:
        return render_template("register.html", error="Käyttäjätunnus on varattu")
    return render_template("login_successful.html")

@app.route("/user")
def user_page():
    if "user_id" not in session:
        return redirect("/login")
    rate_count = ratings.count_ratings_by_user_id(session["user_id"])
    rate_average = ratings.average_by_user_id(session["user_id"])
    rate_average = round(rate_average, 2)
    username = session["username"]
    user_id = session["user_id"]
    user_recipes = recipes.get_user_recipes(user_id)
    return render_template("user.html",username=username,
                           recipes=user_recipes,recipe_count=len(user_recipes),
                           rate_count=rate_count, rate_average=rate_average)

@app.route("/new_recipe")
def new_recipe():
    if "username" not in session:
        return redirect("/login")
    return render_template("new_recipe.html")

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect("/login")
    if request.form.get("csrf_token") != session["csrf_token"]:
        return render_template("error.html",error="Virheellinen pyyntö")
    title = request.form["title"].strip()
    content = request.form["content"].strip()
    categories = request.form.getlist("categories")
    recipe_type = request.form["recipe_type"]
    errors = []
    if not title:
        errors.append("Otsikko ei voi olla tyhjä")
    if not content:
        errors.append("Resepti ei voi olla tyhjä")
    if len(title)>50:
        errors.append("Liian pitkä otsikko")
    if len(content)>10000:
        errors.append("Liian pitkä resepti")
    if errors:
        return render_template("new_recipe.html",
                               errors=errors, title=title,
                               content=content, categories=categories,
                               recipe_type=recipe_type)
    recipes.create_recipe(session["user_id"],
                          title, content, categories, recipe_type)

    return redirect("/user")

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe_by_id(recipe_id)
    rate_count = ratings.count_ratings_by_recipe_id(recipe_id)
    rate_average = ratings.average_by_recipe_id(recipe_id)
    rate_average = round(rate_average, 2)
    if not recipe:
        return render_template("error.html", error="Reseptiä ei löytynyt")
    categories = recipes.get_categorynames_by_recipe_id(recipe_id)
    editable = False
    rate_available = False
    rate = None
    if "user_id" in session:
        editable = session["user_id"] == recipe["creator_id"]
        rate_available = session["user_id"] != recipe["creator_id"]
        if rate_available:
            rate = ratings.get_rating_by_user_id_and_recipe_id(session["user_id"],
                                                               recipe_id)
    return render_template("recipe.html", recipe=recipe, categories=categories,
                           editable=editable, rate_available=rate_available,
                           rate_count=rate_count, rate_average=rate_average,
                           rate=rate)

@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/login")
    recipe = recipes.get_recipe_for_edit(session["user_id"], recipe_id)
    categories = recipes.get_categoryids_by_recipe_id(recipe_id)
    if not recipe:
        return render_template("error.html", error="Ei käyttöoikeutta tähän reseptiin")
    return render_template("edit_recipe.html",recipe=recipe, categories=categories)

@app.route("/update_recipe/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/login")
    if request.form.get("csrf_token") != session["csrf_token"]:
        return render_template("error.html",error="Virheellinen pyyntö")
    categories = request.form.getlist("categories")
    title = request.form["title"].strip()
    content = request.form["content"].strip()
    recipe_type = request.form["recipe_type"]
    errors = []
    if not title:
        errors.append("Otsikko ei voi olla tyhjä")
    if not content:
        errors.append("Resepti ei voi olla tyhjä")
    if len(title)>50:
        errors.append("Liian pitkä otsikko")
    if len(content)>10000:
        errors.append("Liian pitkä resepti")
    if errors:
        return render_template("error.html", errors=errors)
    if not recipes.edit_recipe( session["user_id"],
                               recipe_id, title, content, categories, recipe_type):
        return render_template( "error.html",
                               error="Sinulla ei ole oikeutta muokata tätä reseptiä.")
    return redirect(f"/recipe/{recipe_id}")

@app.route("/delete_recipe/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/login")
    if request.form.get("csrf_token") != session["csrf_token"]:
        return render_template("error.html",error="Virheellinen pyyntö")
    if not recipes.delete_recipe(session["user_id"], recipe_id):
        return render_template("error.html",
                               error="Sinulla ei ole oikeutta poistaa tätä reseptiä.")
    return redirect("/user")

@app.route("/show_user/<int:user_id>")
def show_user(user_id):
    user_recipes = recipes.get_user_recipes(user_id)
    user = users.get_username_from_id(user_id)
    rate_count = ratings.count_ratings_by_user_id(user_id)
    rate_average = ratings.average_by_user_id(user_id)
    rate_average = round(rate_average, 2)
    if not user:
        return render_template("Error.html", error="Käyttäjää ei löytynyt")
    return render_template(
        "show_user.html",
        recipes=user_recipes,
        user=user,
        recipe_count=len(user_recipes),
        rate_count=rate_count,
        rate_average=rate_average)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search_results():
    if request.form.get("csrf_token") != session["csrf_token"]:
        return render_template("error.html",error="Virheellinen pyyntö")
    query = request.form["query"]
    result = recipes.search_recipes_from_title(query)
    return render_template("search.html", recipes=result)

@app.route("/rate_recipe", methods=["POST"])
def rate_recipe():
    if "user_id" not in session:
        return redirect("/login")
    if request.form.get("csrf_token") != session["csrf_token"]:
        return render_template("error.html",error="Virheellinen pyyntö")
    recipe_id = int(request.form["recipe_id"])
    rate = int(request.form["rate"])
    if ratings.rate_recipe(recipe_id, session["user_id"], rate):
        return redirect(f"/recipe/{recipe_id}")
    return render_template("error.html", error="Virheellinen arvio")
