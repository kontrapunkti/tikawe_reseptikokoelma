import sqlite3
import db

def get_user_and_pwhash_by_username(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    return db.query(sql, [username])

def get_username_from_id(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    if len(result) == 0:
        return None
    return result[0]["username"]

def create_user(username, password_hash):
    con = db.connect()

    try:
        sql = """
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
        """
        con.execute(sql, [username, password_hash])

        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()
