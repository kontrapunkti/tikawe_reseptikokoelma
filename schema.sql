CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);

CREATE TABLE IF NOT EXISTS recipes(
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT
);

CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);