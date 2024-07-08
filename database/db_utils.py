import sqlite3


def get_db_connection(db_name="database.db", timeout=10.0):
    conn = sqlite3.connect(db_name, timeout=timeout)
    cursor = conn.cursor()
    return conn, cursor


def close_db_connection(conn):
    conn.commit()
    conn.close()
