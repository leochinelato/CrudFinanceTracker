import sqlite3
from datetime import datetime
from utils.utils import transform_dot_in_comma


def create_tables():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        fullname TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        description VARCHAR(100),
        value REAL,
        date TEXT,
        type TEXT,
        category VARCHAR(100),
        FOREIGN KEY (category) REFERENCES categories(name),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100),
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
        """
    )

    conn.commit()
    conn.close()


def register_new_user(username, fullname, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, fullname, password) VALUES (?,?,?)", (
            username, fullname, password)
    )

    conn.commit()
    conn.close()


def check_if_user_is_registered(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def show_all_transactions_from_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    transactions = cursor.fetchall()

    transactions = [
        {
            "id": t[0],
            "description": t[2],
            "value": transform_dot_in_comma(t[3]),
            "date": datetime.strptime(t[4], "%Y-%m-%d").strftime("%d/%m/%Y"),
            "type": t[5],
        }
        for t in transactions
    ]

    transactions.sort(
        key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"), reverse=True
    )

    conn.close()

    return transactions


def get_user_first_name(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT fullname FROM users WHERE id = ?", (user_id,))
    full_name = cursor.fetchone()

    full_name = full_name[0]
    first_name = full_name.split()[0]

    conn.close()
    return first_name.capitalize()


def get_user_full_name(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fullname FROM users WHERE id = ?", (user_id,))
    full_name = cursor.fetchone()
    full_name = full_name[0]

    conn.close()
    return full_name


def create_new_category_in_db(category_name, user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categories (name, user_id) VALUES (?,?)", (category_name, user_id))

    #     cursor.execute(
    #     "INSERT INTO users (username, fullname, password) VALUES (?,?,?)", (
    #         username, fullname, password)
    # )

    conn.commit()
    conn.close()


def show_all_categories_from_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categories WHERE user_id = ?", (user_id,))
    categories = cursor.fetchall()

    categories = [
        {
            "id": c[0],
            "name": c[1],
        }
        for c in categories
    ]

    conn.close()

    return categories


def store_db(description, user_id, value, date, type):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO transactions (user_id, description,value,date,type)
    VALUES (?,?,?,?,?)
    """,
        (user_id, description, value, date, type),
    )

    conn.commit()
    conn.close()


def update_line(description, value, date, id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE transactions SET description = ?, value = ?, date = ? WHERE id = ?",
        (description, value, date, id),
    )
    conn.commit()
    conn.close()


def remove_line(id):
    conn = sqlite3.connect("database.db")
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


def get_by_id(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM transactions WHERE id = ?", (id,))
    registry = cursor.fetchone()

    return registry


def get_income_sum(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT SUM(value) AS total_income
        FROM transactions
        WHERE type = ?
        AND user_id = ?
        """,
        ("income", user_id),
    )
    total_income = cursor.fetchone()

    conn.close()

    return total_income[0] if total_income[0] else 0


def get_expense_sum(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT SUM(value) AS total_expenses
        FROM transactions
        WHERE type = ?
        AND user_id = ?
        """,
        ("expense", user_id),
    )
    total_expenses = cursor.fetchone()

    conn.close()

    return total_expenses[0] if total_expenses[0] else 0


create_tables()
