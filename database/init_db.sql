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

CREATE TABLE IF NOT EXISTS payments (
    payment_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    service TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    description TEXT,
    payload TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wallet_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    direction TEXT NOT NULL,
    reason TEXT,
    reference TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS registration (
    user_id INTEGER PRIMARY KEY,
    is_registered BOOLEAN
)
