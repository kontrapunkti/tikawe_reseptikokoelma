CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE IF NOT EXISTS recipes(
    id INTEGER PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    title TEXT,
    content TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    edited_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS recipe_categories(
    recipe_id INTEGER REFERENCES recipes,
    category_id INTEGER REFERENCES categories,
    PRIMARY KEY (recipe_id, category_id)
);

CREATE TABLE IF NOT EXISTS ratings(
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    user_id INTEGER REFERENCES users,
    rate INTEGER,
    UNIQUE(recipe_id, user_id)
);

INSERT INTO categories(name) VALUES("Gluteeniton");
INSERT INTO categories(name) VALUES("Laktoositon");
INSERT INTO categories(name) VALUES("Vähälaktoosinen");
INSERT INTO categories(name) VALUES("Vegaaninen");