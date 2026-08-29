import sqlite3

def connect():
    connection = sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = connect()
    with open("schema.sql") as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

def emptytables():
    connection = connect()
    connection.execute("DELETE FROM visits")
    connection.execute("DELETE FROM recipes")
    connection.commit()
    connection.close()

def query(sql, params=[]):
    connection = connect()
    result = connection.execute(sql, params).fetchall()
    connection.close()
    return result
