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


def get_wallet_balance(user_id: int) -> int:
    con = get_connection()
    cur = con.cursor()
    row = cur.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,)).fetchone()
    con.close()
    if row is None or row[0] is None:
        return 0
    return int(round(float(row[0])))


def _add_wallet_transaction(user_id: int, amount: int, direction: str, reason: str, reference: str | None) -> None:
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO wallet_transactions (user_id, amount, direction, reason, reference)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, amount, direction, reason, reference),
    )
    con.commit()
    con.close()


def credit_wallet(user_id: int, amount: int, reason: str, reference: str | None = None) -> int:
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if row is None:
        con.close()
        return 0
    current = int(round(float(row[0] or 0)))
    new_balance = current + int(amount)
    cur.execute("UPDATE users SET wallet = ? WHERE user_id = ?", (new_balance, user_id))
    con.commit()
    con.close()
    _add_wallet_transaction(user_id, int(amount), "credit", reason, reference)
    return new_balance


def debit_wallet(user_id: int, amount: int, reason: str, reference: str | None = None) -> bool:
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if row is None:
        con.close()
        return False
    current = int(round(float(row[0] or 0)))
    amount = int(amount)
    if current < amount:
        con.close()
        return False
    new_balance = current - amount
    cur.execute("UPDATE users SET wallet = ? WHERE user_id = ?", (new_balance, user_id))
    con.commit()
    con.close()
    _add_wallet_transaction(user_id, amount, "debit", reason, reference)
    return True


def create_payment_record(
    payment_id: str,
    user_id: int,
    service: str,
    amount: float,
    currency: str,
    description: str,
    payload: str,
    status: str,
) -> None:
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO payments (payment_id, user_id, service, amount, currency, description, payload, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (payment_id, user_id, service, amount, currency, description, payload, status),
    )
    con.commit()
    con.close()


def get_payment_record(payment_id: str):
    con = get_connection()
    cur = con.cursor()
    row = cur.execute(
        """
        SELECT payment_id, user_id, service, amount, currency, description, payload, status
        FROM payments
        WHERE payment_id = ?
        """,
        (payment_id,),
    ).fetchone()
    con.close()
    if row is None:
        return None
    return {
        "payment_id": row[0],
        "user_id": row[1],
        "service": row[2],
        "amount": row[3],
        "currency": row[4],
        "description": row[5],
        "payload": row[6],
        "status": row[7],
    }


def update_payment_status(payment_id: str, status: str) -> None:
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE payments SET status = ? WHERE payment_id = ?", (status, payment_id))
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
