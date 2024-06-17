import os
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    url_for,
    redirect,
    flash,
    get_flashed_messages,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
from database import (
    register_new_user,
    check_if_user_is_registered,
    store_db,
    show_all_transactions_from_user,
    remove_line,
    get_income_sum,
    get_expense_sum,
    update_line,
    get_by_id,
    get_user_first_name,
)
from utils.utils import transform_dot_in_comma, get_greeting

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET KEY", os.urandom(12).hex())


@ app.route("/user/register", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        username = request.form["username"]
        fullname = request.form["fullname"]
        password = generate_password_hash(request.form["password"])
        register_new_user(username, fullname, password)
        return redirect(url_for("login"))

    return render_template("register.html")


@ app.route("/user/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = check_if_user_is_registered(username)

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            return redirect(url_for("index"))
        flash(f"Username not exists or invalid password.", "error")
    return render_template("login.html")


@ app.route("/user/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@ app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    first_name = get_user_first_name(session["user_id"])
    greeting = get_greeting(first_name)
    data = show_all_transactions_from_user(session["user_id"])
    total_income, total_expense = get_income_sum(session["user_id"]), get_expense_sum(
        session["user_id"]
    )
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


@ app.route("/new", methods=["POST", "GET"])
def create_new_transaction():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        try:
            user_id = session["user_id"]
            description = request.form["description"]
            value = float(request.form["value"])
            date = request.form["date"]
            type = request.form["type"]
        except ValueError:
            flash(f"Erro ao cadastrar a transação: 'Valor' Deve ser numérico.", "error")
            return redirect(url_for("form_new_item"))

        store_db(
            user_id=user_id,
            description=description,
            value=value,
            date=date,
            type=type,
        )
        return redirect(url_for("index"))
    return render_template("form_new_item.html")


@ app.route("/update/<int:id>", methods=["POST", "GET"])
def update_transaction(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            description = request.form["description"]
            value = float(request.form["value"])
            date = request.form["date"]
        except:
            flash(f"Erro ao editar a transação: 'Valor' Deve ser numérico.", "error")
            return redirect(url_for("form_edit_transaction", transaction_id=id))

        edited_transaction = update_line(description, value, date, id)

        return redirect(url_for("index"))

    transaction = get_by_id(id)

    transaction = {
        "id": transaction[0],
        "description": transaction[2],
        "amount": transaction[3],
        "date": transaction[4],
        "type": transaction[5],
    }

    return render_template("form_new_item.html", transaction=transaction)


@ app.route("/delete", methods=["POST"])
def delete_transaction():
    id = request.form["id"]

    remove_line(id)

    return redirect(url_for("index"))


if __name__ == "__main__":

    app.run(port=8000, debug=True)
