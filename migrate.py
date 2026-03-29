#!/usr/bin/env python3
"""
Скрипт миграции существующей БД для Mini App
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = "database/falt.db"  # Укажите ваш путь

def migrate():
    print("🔄 Начинаем миграцию базы данных...")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Проверяем существующие таблицы
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing = [row[0] for row in cur.fetchall()]

    print(f"Найдены таблицы: {existing}")

    # Добавляем колонку email в users
    if 'users' in existing:
        try:
            cur.execute("ALTER TABLE users ADD COLUMN email TEXT UNIQUE")
            print("✅ Добавлена колонка email в users")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ Колонка email уже существует")
            else:
                print(f"⚠️ Ошибка: {e}")

    # Добавляем колонки в laundry
    if 'laundry' in existing:
        columns_to_add = [
            ("machine_id", "TEXT"),
            ("date", "TEXT"),
            ("status", "TEXT DEFAULT 'active'")
        ]
        for col, type_ in columns_to_add:
            try:
                cur.execute(f"ALTER TABLE laundry ADD COLUMN {col} {type_}")
                print(f"✅ Добавлена колонка {col} в laundry")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"ℹ️ Колонка {col} уже существует")
                else:
                    print(f"⚠️ Ошибка: {e}")

    # Создаем новые таблицы
    new_tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS mini_app_sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            auth_token TEXT UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT NOT NULL,
            last_activity TEXT DEFAULT CURRENT_TIMESTAMP,
            device_info TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action_type TEXT NOT NULL,
            source TEXT NOT NULL,
            payload TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS time_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            machine_id TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            is_available BOOLEAN DEFAULT 1,
            booked_by INTEGER,
            booking_id INTEGER,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date, machine_id, start_time)
        )
        """
    ]

    table_names = ['mini_app_sessions', 'sync_log', 'time_slots']

    for i, create_sql in enumerate(new_tables_sql):
        table_name = table_names[i]
        if table_name not in existing:
            cur.execute(create_sql)
            print(f"✅ Создана таблица {table_name}")
        else:
            print(f"ℹ️ Таблица {table_name} уже существует")

    # Создаем индексы
    indexes = [
        ("idx_users_email", "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)"),
        ("idx_laundry_user_date", "CREATE INDEX IF NOT EXISTS idx_laundry_user_date ON laundry(user_id, date)"),
        ("idx_time_slots_date_machine", "CREATE INDEX IF NOT EXISTS idx_time_slots_date_machine ON time_slots(date, machine_id)")
    ]

    for idx_name, create_sql in indexes:
        try:
            cur.execute(create_sql)
            print(f"✅ Создан индекс {idx_name}")
        except Exception as e:
            print(f"⚠️ Ошибка создания индекса {idx_name}: {e}")

    # Обновляем существующие записи laundry
    try:
        cur.execute("UPDATE laundry SET status = 'active' WHERE status IS NULL")
        print("✅ Обновлены статусы существующих бронирований")
    except Exception as e:
        print(f"⚠️ Ошибка обновления статусов: {e}")

    conn.commit()
    conn.close()

    print("\n✅ Миграция завершена успешно!")
    print("Теперь можно запускать Mini App.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        DB_PATH = sys.argv[1]

    if not Path(DB_PATH).exists():
        print(f"❌ База данных не найдена: {DB_PATH}")
        print("Создаем новую базу данных...")
        from database.db_mini_app import init_db
        init_db()
    else:
        migrate()
