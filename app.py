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
    get_user_full_name,
    show_all_categories_from_user,
    create_new_category_in_db,
)
from utils.utils import transform_dot_in_comma, get_greeting
from decorators import login_required

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
        next_url = request.form["next"]

        user = check_if_user_is_registered(username)

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            if next_url:
                return redirect(next_url)
            return redirect(url_for("index"))
        flash(f"Username not exists or invalid password.", "error")
    return render_template("login.html")


@ app.route("/user/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@ app.route("/")
@login_required
def index():

    user_id = session["user_id"]
    full_name = get_user_full_name(user_id)
    greeting = get_greeting()
    data = show_all_transactions_from_user(user_id)
    total_income, total_expense = get_income_sum(user_id), get_expense_sum(
        user_id
    )
    total_balance = total_income - total_expense
    print(data)

    return render_template(
        "index.html",
        data=data,
        total_income=transform_dot_in_comma(total_income),
        total_expense=transform_dot_in_comma(total_expense),
        total_balance=transform_dot_in_comma(total_balance),
        greeting=greeting,
        edit=True,
        full_name=full_name
    )


@app.route("/month")
@login_required
def show_transactions_by_month():
    return render_template("transactions_by_month.html")


@app.route("/new", methods=["POST", "GET"])
@login_required
def create_new_transaction():
    if request.method == "POST":
        try:
            user_id = session["user_id"]
            description = request.form["description"]
            value = float(request.form["value"])
            date = request.form["date"]
            type = request.form["type"]
            category = request.form["category"]
        except ValueError:
            flash(f"Erro ao cadastrar a transação: 'Valor' Deve ser numérico.", "error")
            return redirect(url_for("form_new_item"))

        store_db(
            user_id=user_id,
            description=description,
            value=value,
            date=date,
            type=type,
            category=category
        )
        return redirect(url_for("index"))

    categories = show_all_categories_from_user(session["user_id"])
    return render_template("form_new_item.html", categories=categories)


@ app.route("/update/<int:id>", methods=["POST", "GET"])
@login_required
def update_transaction(id):
    if request.method == "POST":
        try:
            description = request.form["description"]
            value = float(request.form["value"])
            date = request.form["date"]
            category = request.form["category"]
        except:
            flash(f"Erro ao editar a transação: 'Valor' Deve ser numérico.", "error")
            return redirect(url_for("form_edit_transaction", transaction_id=id))

        edited_transaction = update_line(
            description, value, date, category, id)

        return redirect(url_for("index"))

    transaction = get_by_id(id)

    transaction = {
        "id": transaction[0],
        "description": transaction[2],
        "amount": transaction[3],
        "date": transaction[4],
        "type": transaction[5],
    }

    categories = show_all_categories_from_user(session["user_id"])
    return render_template("form_new_item.html", transaction=transaction, categories=categories)


@ app.route("/delete", methods=["POST"])
@login_required
def delete_transaction():
    id = request.form["id"]
    remove_line(id)

    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def show_user_profile():
    full_name = get_user_full_name(session["user_id"])
    return render_template("profile.html", full_name=full_name)


@app.route("/categories")
@login_required
def show_categories():
    user_id = session["user_id"]
    transactions = show_all_transactions_from_user(user_id)
    categories = show_all_categories_from_user(user_id)

    return render_template("categories.html", categories=categories)


@app.route("/categories/new", methods=["POST", "GET"])
@login_required
def create_new_category():
    if request.method == "POST":
        user_id = session["user_id"]
        category_name = request.form["category-name"]
        create_new_category_in_db(category_name, user_id)
        return redirect(url_for("show_categories"))

    return render_template("form_new_category.html")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
