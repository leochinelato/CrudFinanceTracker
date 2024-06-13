from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    url_for,
    redirect,
    flash,
    get_flashed_messages,
)
from database import (
    store_db,
    get_all_data,
    remove_line,
    get_income_sum,
    get_expense_sum,
    update_line,
    get_by_id,
)
from utils.utils import transform_dot_in_comma, get_greeting

# COLOCAR CATEGORIA

app = Flask(__name__)
app.secret_key = "9i0fewmi90dma d09m k kd as batata azul"


@app.route("/")
def index():
    greeting = get_greeting()
    data = get_all_data()
    total_income, total_expense = get_income_sum(), get_expense_sum()
    total_balance = total_income - total_expense

    return render_template(
        "index.html",
        data=data,
        total_income=transform_dot_in_comma(total_income),
        total_expense=transform_dot_in_comma(total_expense),
        total_balance=transform_dot_in_comma(total_balance),
        greeting=greeting,
        edit=True,
    )


@app.route("/create", methods=["GET"])
def form_new_item():
    return render_template("form_new_item.html")


@app.route("/new", methods=["POST"])
def create_new_transaction():
    try:
        description = request.form["description"]
        value = float(request.form["value"])
        date = request.form["date"]
        type = request.form["type"]
    except ValueError:
        flash(f"Erro ao cadastrar a transação: 'Valor' Deve ser numérico.", "error")
        return redirect(url_for("form_new_item"))

    store_db(
        description=description,
        value=value,
        date=date,
        type=type,
    )
    return redirect(url_for("index"))


@app.route("/edit/<int:transaction_id>")
def form_edit_transaction(transaction_id):
    transaction = get_by_id(transaction_id)

    transaction = {
        "id": transaction[0],
        "description": transaction[1],
        "amount": transaction[2],
        "date": transaction[3],
        "type": transaction[4],
    }

    return render_template("form_new_item.html", transaction=transaction)


@app.route("/update/<int:id>", methods=["POST"])
def update_transaction(id):

    try:
        description = request.form["description"]
        value = float(request.form["value"])
        date = request.form["date"]
    except:
        flash(f"Erro ao editar a transação: 'Valor' Deve ser numérico.", "error")
        return redirect(url_for("form_edit_transaction", transaction_id=id))

    edited_transaction = update_line(description, value, date, id)

    return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete_transaction():
    id = request.form["id"]

    remove_line(id)

    return redirect(url_for("index"))


if __name__ == "__main__":

    app.run(port=8000, debug=True)
