import sqlite3
from datetime import datetime
from utils.utils import transform_dot_in_comma


def create_tables():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY,
        descricao TEXT,
        valor REAL,
        data TEXT
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY,
        descricao TEXT,
        valor REAL,
        data TEXT
    )
    """
    )

    conn.commit()
    conn.close()


def store_db(descricao, valor_transacao, data_transacao, tipo_transacao):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    if tipo_transacao == "receita":
        cursor.execute(
            """
        INSERT INTO receitas (descricao,valor,data)
        VALUES (?,?,?)
        """,
            (descricao, valor_transacao, data_transacao),
        )
    elif tipo_transacao == "despesa":
        cursor.execute(
            """
        INSERT INTO despesas (descricao,valor,data)
        VALUES (?,?,?)""",
            (descricao, abs(valor_transacao), data_transacao),
        )

    conn.commit()
    conn.close()


def update_line(tabela, descricao, valor_transacao, data_transacao, id_transacao):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE {tabela} SET descricao = ?, valor = ?, data = ? WHERE id = ?",
        (descricao, valor_transacao, data_transacao, id_transacao),
    )
    conn.commit()
    conn.close()


def remove_line(tabela, valor):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    try:
        query = f"DELETE FROM {tabela} WHERE id = ?"
        cursor.execute(query, (valor,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao remover linha: {e}")
    finally:
        cursor.close()
        conn.close()


def get_all_data():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM receitas")
    receitas = cursor.fetchall()

    receitas = [
        {
            "id": r[0],
            "description": r[1],
            "amount": transform_dot_in_comma(r[2]),
            "date": datetime.strptime(r[3], "%Y-%m-%d").strftime("%d/%m/%Y"),
            "type": "receita",
        }
        for r in receitas
    ]

    cursor.execute("SELECT * FROM despesas")
    despesas = cursor.fetchall()

    despesas = [
        {
            "id": d[0],
            "description": d[1],
            "amount": transform_dot_in_comma(d[2]),
            "date": datetime.strptime(d[3], "%Y-%m-%d").strftime("%d/%m/%Y"),
            "type": "despesa",
        }
        for d in despesas
    ]

    combined = receitas + despesas
    combined.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"), reverse=True)

    conn.close()

    return combined


def get_by_id(id, tabela):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {tabela}s WHERE id = ?", (id,))
    registro = cursor.fetchone()

    return registro


def get_receitas_sum():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(valor) AS total_receitas FROM receitas")
    total_receitas = cursor.fetchone()

    conn.close()

    return total_receitas[0] if total_receitas[0] else 0


def get_despesas_sum():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(valor) AS total_despesas FROM despesas")
    total_despesas = cursor.fetchone()

    conn.close()

    return total_despesas[0] if total_despesas[0] else 0


create_tables()
