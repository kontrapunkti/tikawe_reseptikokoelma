import random
from datetime import datetime, timedelta

import db
from werkzeug.security import generate_password_hash

con = db.connect()
con.execute("DELETE FROM recipes")
con.execute("DELETE FROM users")

usernames = [
    "kalle",
    "maija",
    "pekka",
    "matti",
    "liisa",
    "anna",
    "jari",
    "minna",
    "teemu",
    "sara"
]

for username in usernames:
    try:
        con.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            [username, generate_password_hash("salasana")]
        )
    except:
        pass

# Hae käyttäjät
users = con.execute(
    "SELECT id, username FROM users"
).fetchall()

recipe_names = [
    "Lohikeitto",
    "Makaronilaatikko",
    "Pinaattikeitto",
    "Kanapasta",
    "Kasvissosekeitto",
    "Mustikkapiirakka",
    "Pannukakku",
    "Hernekeitto",
    "Jauhelihakastike",
    "Uunilohi"
]

for i in range(100):
    type_id = random.randint(1, 3)
    user = random.choice(users)

    created_at = (
        datetime.now()
        - timedelta(days=random.randint(0, 365))
    ).strftime("%Y-%m-%d %H:%M:%S")

    title = f"{random.choice(recipe_names)} #{i+1}"

    content = f"""
Ainekset:
- 500 g pääraaka-ainetta
- 2 dl vettä
- mausteita maun mukaan

Valmistus:
1. Sekoita ainekset.
2. Kypsennä.
3. Tarjoile.
"""

    con.execute("""
        INSERT INTO recipes (creator_id, title, content, type_id, created_at, edited_at)
        VALUES (?, ?, ?, ?, ?, ?) """,
        [user["id"], title, content, type_id, created_at, created_at])

con.commit()
con.close()