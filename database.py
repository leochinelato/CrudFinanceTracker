import sqlite3
from datetime import datetime
from utils.utils import transform_dot_in_comma


def create_tables():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        description TEXT,
        value REAL,
        date TEXT,
        type TEXT
    )
    """
    )

    conn.commit()
    conn.close()


def store_db(description, value, date, type):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO transactions (description,value,date,type)
    VALUES (?,?,?,?)
    """,
        (description, value, date, type),
    )

    conn.commit()
    conn.close()


def update_line(description, value, date, id):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE transactions SET description = ?, value = ?, date = ? WHERE id = ?",
        (description, value, date, id),
    )
    conn.commit()
    conn.close()


def remove_line(id):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    try:
        query = f"DELETE FROM transactions WHERE id = ?"
        cursor.execute(query, (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error removing transaction: {e}")
    finally:
        cursor.close()
        conn.close()


def get_all_data():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()

    transactions = [
        {
            "id": t[0],
            "description": t[1],
            "value": transform_dot_in_comma(t[2]),
            "date": datetime.strptime(t[3], "%Y-%m-%d").strftime("%d/%m/%Y"),
            "type": t[4],
        }
        for t in transactions
    ]

    transactions.sort(
        key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"), reverse=True
    )

    conn.close()

    return transactions


def get_by_id(id):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM transactions WHERE id = ?", (id,))
    registry = cursor.fetchone()

    return registry


def get_income_sum():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(value) AS total_income FROM transactions WHERE type = ?",
        ("income",),
    )
    total_income = cursor.fetchone()

    conn.close()

    return total_income[0] if total_income[0] else 0


def get_expense_sum():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(value) AS total_expenses FROM transactions where type = ?",
        ("expense",),
    )
    total_expenses = cursor.fetchone()

    conn.close()

    return total_expenses[0] if total_expenses[0] else 0


create_tables()
