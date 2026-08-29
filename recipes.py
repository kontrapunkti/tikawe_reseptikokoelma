import db

def get_user_recipes(user_id):
    sql = """
    SELECT id, title
    FROM recipes
    WHERE creator_id = ?
    ORDER BY edited_at DESC, created_at DESC
    """

    return db.query(sql, [user_id])

def create_recipe(creator_id, title, content, categories, recipe_type):
    con = db.connect()
    cursor = con.execute("""INSERT INTO recipes (creator_id, title, content, type_id)
                        VALUES (?, ?, ?, ?)""",
                        [creator_id, title.title(), content, recipe_type])
    if categories:
        for category_id in categories:
            con.execute("INSERT INTO recipe_categories (recipe_id, category_id) VALUES (?, ?)",
                        [cursor.lastrowid, category_id])
    con.commit()
    con.close()

def get_recipe_by_id(recipe_id):
    result = db.query("""
        SELECT R.id, R.creator_id, R.title, R.content, RT.name AS recipe_type,  U.username
        FROM recipes R
        LEFT JOIN users U ON U.id = R.creator_id
        LEFT JOIN recipe_types RT ON R.type_id = RT.id
        WHERE R.id = ?""", [recipe_id])

    if len(result)==0:
        return None   
    return result[0]

def get_recipe_for_edit(user_id, recipe_id):
    result = db.query("""
            SELECT id, title, content, type_id
            FROM recipes
            WHERE creator_id = ?
            AND id = ?""", [user_id, recipe_id])

    if len(result) == 0:
        return None

    return result[0]

def edit_recipe(user_id, recipe_id, title, content, categories, recipe_type):
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
        SET title = ?, content = ?, edited_at = CURRENT_TIMESTAMP, type_id = ?
        WHERE id = ?"""
    con.execute(sql, [title.title(), content, recipe_type, recipe_id])
    con.execute("DELETE FROM recipe_categories WHERE recipe_id = ?", [recipe_id])
    for category_id in categories:
        con.execute("INSERT INTO recipe_categories (recipe_id, category_id) VALUES (?, ?)",
                    [recipe_id, category_id])
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
    con.execute("DELETE FROM recipe_categories WHERE recipe_id = ?", [recipe_id])
    con.execute("DELETE FROM ratings WHERE recipe_id = ?", [recipe_id])
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

def get_categoryids_by_recipe_id(recipe_id):
    result = db.query("""
        SELECT category_id
        FROM recipe_categories
        WHERE recipe_id = ?""", [recipe_id])
    ids = []
    for cat_id in result:
        ids.append(cat_id["category_id"])
    return ids

def get_categorynames_by_recipe_id(recipe_id):
    result = db.query("""
        SELECT name
        FROM categories
        LEFT JOIN recipe_categories
        ON categories.id = recipe_categories.category_id
        WHERE recipe_categories.recipe_id = ?""", [recipe_id])
    names = []
    for cat_id in result:
        names.append(cat_id["name"])
    return names
