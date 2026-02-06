import sqlite3
from config import DB_PATH as DATABASE_PATH

class User():
    def __init__(self, user_id, name, surname, wallet = 0, label = 0):
        self.name = name
        self.surname = surname
        self.user_id = user_id
        self.wallet = wallet
        self.label = label

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(open("database/init_db.sql", "r", encoding="utf8").read())
    conn.commit()
    conn.close()

def add_user(user : User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, name, surname, wallet, label) VALUES (?, ?, ?, ?, ?)",
                   (user.user_id, user.name, user.surname, user.wallet, user.label, ))
    conn.commit()
    conn.close()

def is_registered(user_id) -> User | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id == ? LIMIT 1", (user_id, ))
    user = cursor.fetchone()
    conn.close()
    if user is not None:
        return User(user_id = user[1], name = user[2], surname = user[3], wallet=user[4], label=user[5])
    return None


def get_machine_names() -> list[str]:
    con = get_connection()
    cur = con.cursor()
    machine_names = cur.execute("SELECT name FROM washing_machines ORDER BY name ASC").fetchall()
    con.close()
    return [i[0] for i in machine_names]


def get_machine_status(machine_name: str) -> bool:
    con = get_connection()
    cur = con.cursor()
    machine_status = cur.execute("SELECT is_working FROM washing_machines WHERE name = ?", (machine_name, )).fetchone()
    con.close()
    return machine_status[0]


def change_machine_status(machine_name: str) -> None:
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE washing_machines SET is_working = not is_working WHERE name = ?", (machine_name, ))
    con.commit()
    con.close()
def add_registration_click(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registration (user_id, is_registered) VALUES (?, ?)",
                   (user_id, True, ))
    conn.commit()
    conn.close()


def registration_clicked(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM registration WHERE user_id == ?", (user_id,)).fetchone()
    if not user or not user[1]:
        return False
    return True


def set_registration_click_status(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE registration SET is_registered = NOT(SELECT is_registered FROM registration WHERE user_id == ?) WHERE user_id == ?", (user_id, user_id))
    conn.commit()
    conn.close()
