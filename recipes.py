import db
import datetime

def get_user_recipes(user_id):
    sql = """
    SELECT id, title
    FROM recipes
    WHERE creator_id = ?
    """

    return db.query(sql, [user_id])

def create_recipe(creator_id, title, content):
    con = db.connect()
    con.execute("INSERT INTO recipes (creator_id, title, content) VALUES (?, ?, ?)",
        [creator_id, title.title(), content])
    con.commit()
    con.close()

def get_recipe_by_id(recipe_id):
    result = db.query("""
        SELECT R.id, R.creator_id, R.title, R.content, U.username
        FROM recipes R
        LEFT JOIN users U ON U.id = R.creator_id
        WHERE R.id = ?""", [recipe_id])

    if len(result)==0:
        return None
    
    return result[0]

def get_recipe_for_edit(user_id, recipe_id):
    result = db.query("""
            SELECT id, title, content
            FROM recipes
            WHERE creator_id = ?
            AND id = ?""", [user_id, recipe_id])

    if len(result) == 0:
        return None

    return result[0]

def edit_recipe(user_id, recipe_id, title, content):
    result = db.query("""
            SELECT id
            FROM recipes
            WHERE creator_id = ?
            AND id = ?""", [user_id, recipe_id])

    if len(result) == 0:
        return False

    con = db.connect()
    sql = """
    UPDATE recipes
    SET title = ?, content = ?, edited_at = CURRENT_TIMESTAMP
    WHERE id = ?"""
    con.execute(sql, [title.title(), content, recipe_id])
    con.commit()
    con.close()
    return True

def delete_recipe(user_id, recipe_id):
    result = db.query("""
            SELECT id
            FROM recipes
            WHERE creator_id = ?
            AND id = ?""", [user_id, recipe_id])

    if len(result) == 0:
        return False
    con = db.connect()
    con.execute("DELETE FROM recipes WHERE id = ?", [recipe_id])
    con.commit()
    con.close()
    return True

def search_recipes_from_title(query):
    return db.query("""
            SELECT id, title
            FROM recipes
            WHERE title LIKE ?
        """, [f'%{query}%'])

def get_recent_recipes(count):
    return db.query("""
        SELECT id, title, created_at
        FROM recipes
        ORDER BY created_at DESC
        LIMIT ?
        """, [count])