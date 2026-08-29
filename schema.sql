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
    type_id INTEGER REFERENCES recipe_types,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    edited_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS recipe_categories(
    recipe_id INTEGER REFERENCES recipes,
    category_id INTEGER REFERENCES categories,
    PRIMARY KEY (recipe_id, category_id)
);

CREATE TABLE IF NOT EXISTS recipe_types(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS ratings(
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    user_id INTEGER REFERENCES users,
    rate INTEGER,
    UNIQUE(recipe_id, user_id)
);

INSERT OR IGNORE INTO categories(name) VALUES('Gluteeniton');
INSERT OR IGNORE INTO categories(name) VALUES('Laktoositon');
INSERT OR IGNORE INTO categories(name) VALUES('Vähälaktoosinen');
INSERT OR IGNORE INTO categories(name) VALUES('Vegaaninen');

INSERT OR IGNORE INTO recipe_types(name) VALUES('Alkuruoka');
INSERT OR IGNORE INTO recipe_types(name) VALUES('Pääruoka');
INSERT OR IGNORE INTO recipe_types(name) VALUES('Jälkiruoka');