DROP TABLE IF EXISTS visits;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS users;

CREATE TABLE visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);

CREATE TABLE recipes(
    id INTEGER PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    title TEXT,
    content TEXT
);

CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);