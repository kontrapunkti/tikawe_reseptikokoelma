import db

def rate_recipe(recipe_id, user_id, rate):
    if rate < 1 or rate > 5:
        return False
    result = db.query("""SELECT id FROM ratings WHERE recipe_id = ? AND user_id = ?""",
                      [recipe_id, user_id])
    con = db.connect()
    try:
        if len(result) == 0:
            con.execute("INSERT INTO ratings (recipe_id, user_id, rate) VALUES (?, ?, ?)",
                        [recipe_id, user_id, rate])
            con.commit()
        else:
            con.execute("UPDATE ratings SET rate = ? WHERE recipe_id = ? AND user_id = ?",
                        [rate, recipe_id, user_id])
            con.commit()
    finally:
        con.close()
    return True

def average_by_recipe_id(recipe_id):
    avg = db.query("SELECT AVG(rate) AS avg FROM ratings WHERE recipe_id = ?",
                   [recipe_id])[0]["avg"]
    if avg is None:
        return 0
    return avg

def count_ratings_by_recipe_id(recipe_id):
    return db.query("SELECT COUNT(id) AS count FROM ratings WHERE recipe_id = ?",
                    [recipe_id])[0]["count"]

def average_by_user_id(user_id):
    avg = db.query("""
        SELECT AVG(ratings.rate) AS avg
        FROM ratings, recipes
        WHERE ratings.recipe_id = recipes.id
        AND recipes.creator_id = ?
        """, [user_id])[0]["avg"]
    if avg is None:
        return 0
    return avg

def count_ratings_by_user_id(user_id):
    return db.query("""SELECT COUNT(ratings.id) AS count FROM ratings, recipes
        WHERE ratings.recipe_id = recipes.id AND recipes.creator_id = ?""",
        [user_id])[0]["count"]

def get_rating_by_user_id_and_recipe_id(user_id, recipe_id):
    result = db.query("SELECT rate FROM ratings WHERE user_id = ? AND recipe_id = ?",
                    [user_id, recipe_id])
    if len(result) == 0:
        return None
    return result[0]["rate"]