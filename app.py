from flask import Flask, render_template, request, jsonify, url_for, redirect
from database import (
    store_db,
    get_all_data,
    remove_line,
    get_receitas_sum,
    get_despesas_sum,
)
from utils.utils import transform_dot_in_comma, get_greeting

# COLOCAR CATEGORIA

app = Flask(__name__)


@app.route("/")
def index():
    greeting = get_greeting()
    data = get_all_data()
    total_receitas, total_despesas = get_receitas_sum(), get_despesas_sum()
    saldo_total = total_receitas - total_despesas
    return render_template(
        "index.html",
        data=data,
        total_receitas=transform_dot_in_comma(total_receitas),
        total_despesas=transform_dot_in_comma(total_despesas),
        saldo_total=transform_dot_in_comma(saldo_total),
        greeting=greeting,
        edit=True,
    )


@app.route("/new", methods=["POST"])
def create_new_transaction():
    description = request.form["description"]
    value = float(request.form["value"])
    date = request.form["date"]
    tipo_transacao = request.form["tipo_transacao"]
    store_db(
        descricao=description,
        valor_transacao=value,
        data_transacao=date,
        tipo_transacao=tipo_transacao,
    )
    return redirect(url_for("index"))


@app.route("/update/<int:id>", methods=["PUT"])
def update_transaction():
    description = request.form["description"]
    value = float(request.form["value"])
    date = request.form["date"]
    tipo_transacao = request.form["tipo_transacao"]
    return jsonify({"msg": "ok"})


@app.route("/delete", methods=["POST"])
def delete_transaction():
    tabela = request.form["tabela"]
    id = request.form["id"]

    remove_line(tabela, id)

    return redirect(url_for("index"))


if __name__ == "__main__":

    app.run(port=8000, debug=True)
