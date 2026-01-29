CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    name TEXT,
    surname TEXT,
    wallet REAL DEFAULT 0,
    label TEXT
);

CREATE TABLE IF NOT EXISTS laundry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    start_time TEXT,
    end_time TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);


CREATE TABLE IF NOT EXISTS washing_machines (
    name TEXT PRIMARY KEY,
    is_working BOOLEAN NOT NULL
);


INSERT OR IGNORE INTO washing_machines (name, is_working) VALUES
('#1', 1),
('#2', 1),
('#3', 1),
('#4', 0),
('#5', 1),
('#6 (Сушилка)', 1);

