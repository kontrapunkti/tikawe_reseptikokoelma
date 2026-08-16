DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS users;


CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes(
    id INTEGER PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    title TEXT,
    content TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    edited_at TEXT DEFAULT CURRENT_TIMESTAMP
);