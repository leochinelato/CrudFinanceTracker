import sqlite3
from datetime import datetime
from utils.utils import transform_dot_in_comma
from database.db_utils import get_db_connection, close_db_connection


def create_tables():
    conn, cursor = get_db_connection()

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
        total_value REAL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
        """
    )

    close_db_connection(conn)


def create_triggers():
    conn, cursor = get_db_connection()

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_category_total_on_insert
        AFTER INSERT ON transactions
        FOR EACH ROW
        BEGIN
            UPDATE categories
            SET total_value = total_value + NEW.value
            WHERE name = NEW.category;
        END;
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_category_total_on_update
        AFTER UPDATE OF value, category on transactions
        FOR EACH ROW
        BEGIN
            UPDATE categories
            SET total_value = total_value = OLD.value
            WHERE name = OLD.category;

            UPDATE categories
            SET total_value = total_value + NEW.value
            WHERE name = NEW.category;
        END;
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_category_total_on_delete
        AFTER DELETE ON transactions
        FOR EACH ROW
        BEGIN
            UPDATE categories
            SET total_value = total_value - OLD.value
            WHERE name = OLD.category;
        END;
    """)

    close_db_connection(conn)


def register_new_user(username, fullname, password):
    conn, cursor = get_db_connection()

    cursor.execute(
        "INSERT INTO users (username, fullname, password) VALUES (?,?,?)", (
            username, fullname, password)
    )

    close_db_connection(conn)


def edit_user_profile(username, fullname, id):
    conn, cursor = get_db_connection()

    cursor.execute(
        f"UPDATE users SET username = ?, fullname = ? WHERE id = ?",
        (username, fullname, id),
    )

    close_db_connection(conn)


def get_user_by_id(id):
    conn, cursor = get_db_connection()

    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()
    return user


def check_if_user_is_registered(username):
    conn, cursor = get_db_connection()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def show_all_transactions_from_user(user_id):
    conn, cursor = get_db_connection()

    cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    transactions = cursor.fetchall()

    transactions = [
        {
            "id": t[0],
            "description": t[2],
            "value": transform_dot_in_comma(t[3]),
            "date": datetime.strptime(t[4], "%Y-%m-%d").strftime("%d/%m/%Y"),
            "type": t[5],
            "category": t[6],
        }
        for t in transactions
    ]

    transactions.sort(
        key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"), reverse=True
    )

    conn.close()

    return transactions


def get_user_full_name(user_id):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT fullname FROM users WHERE id = ?", (user_id,))
    full_name = cursor.fetchone()
    full_name = full_name[0].title()

    conn.close()
    return full_name


def create_new_category_in_db(category_name, user_id):
    conn, cursor = get_db_connection()

    cursor.execute(
        "INSERT INTO categories (name, user_id) VALUES (?,?)", (category_name, user_id))

    close_db_connection(conn)


def show_all_categories_from_user(user_id):
    conn, cursor = get_db_connection()

    cursor.execute("SELECT * FROM categories WHERE user_id = ?", (user_id,))
    categories = cursor.fetchall()

    categories = [
        {
            "id": c[0],
            "name": c[1],
            "total_value": c[3],
        }
        for c in categories
    ]

    conn.close()

    return categories


def store_db(description, user_id, value, date, type, category):
    conn, cursor = get_db_connection()

    cursor.execute(
        """
    INSERT INTO transactions (user_id, description,value,date,type,category)
    VALUES (?,?,?,?,?,?)
    """,
        (user_id, description, value, date, type, category),
    )

    close_db_connection(conn)


def update_line(description, value, date, category, id):
    conn, cursor = get_db_connection()

    cursor.execute(
        f"UPDATE transactions SET description = ?, value = ?, date = ?, category = ? WHERE id = ?",
        (description, value, date, category, id),
    )

    close_db_connection(conn)


def remove_line(id):
    conn, cursor = get_db_connection()

    try:
        query = f"DELETE FROM transactions WHERE id = ?"
        cursor.execute(query, (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error removing transaction: {e}")
    finally:
        close_db_connection(conn)


def get_by_id(id):
    conn, cursor = get_db_connection()

    cursor.execute(f"SELECT * FROM transactions WHERE id = ?", (id,))
    registry = cursor.fetchone()

    return registry


def get_income_sum(user_id):
    conn, cursor = get_db_connection()

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
    conn, cursor = get_db_connection()

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


def setup_database():
    create_tables()
    create_triggers()
