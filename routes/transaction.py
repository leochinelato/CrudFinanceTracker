from flask import Blueprint, session, render_template, flash, url_for, request, redirect
from database.database import store_db, get_user_full_name, show_all_transactions_from_user, get_income_sum, get_expense_sum, show_all_categories_from_user, update_line, get_by_id, remove_line
from utils.utils import get_greeting, transform_dot_in_comma
from decorators import login_required

transaction_route = Blueprint("transaction", __name__)


@transaction_route.route("/")
@login_required
def index():

    user_id = session["user_id"]
    full_name = get_user_full_name(user_id)
    greeting = get_greeting()
    data = show_all_transactions_from_user(user_id)
    total_income, total_expense = get_income_sum(
        user_id), get_expense_sum(user_id)
    total_balance = total_income - total_expense

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


@transaction_route.route("/transactions")
@login_required
def show_transactions():
    user_id = session["user_id"]
    transactions = show_all_transactions_from_user(user_id)
    return render_template("transactions.html", transactions=transactions)


@transaction_route.route("/new", methods=["POST", "GET"])
@login_required
def create_new_transaction():
    if request.method == "POST":
        try:
            user_id = session["user_id"]
            description = request.form["description"]
            value = float(request.form["value"])
            date = request.form["date"]
            type = request.form["type"]
            category = request.form.get("category")
        except ValueError:
            flash(f"Erro ao cadastrar a transação: 'Valor' Deve ser numérico.", "error")

        store_db(
            user_id=user_id,
            description=description,
            value=value,
            date=date,
            type=type,
            category=category
        )
        return redirect(url_for("transaction.index"))

    categories = show_all_categories_from_user(session["user_id"])
    return render_template("form_new_item.html", categories=categories)


@transaction_route.route("/update/<int:id>", methods=["POST", "GET"])
@login_required
def update_transaction(id):
    if request.method == "POST":
        try:
            description = request.form["description"]
            value = float(request.form["value"])
            date = request.form["date"]
            category = request.form.get("category")
        except:
            flash(f"Erro ao editar a transação: 'Valor' Deve ser numérico.", "error")
            return redirect(url_for("transaction.form_edit_transaction", transaction_id=id))

        edited_transaction = update_line(
            description, value, date, category, id)

        return redirect(url_for("transaction.index"))

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


@transaction_route.route("/delete", methods=["POST"])
@login_required
def delete_transaction():
    id = request.form["id"]
    remove_line(id)

    return redirect(url_for("transaction.index"))
