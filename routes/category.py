from flask import Blueprint, render_template, request, session, url_for, redirect
from decorators import login_required
from database.database import show_all_transactions_from_user, show_all_categories_from_user, create_new_category_in_db

category_route = Blueprint("category", __name__)


@category_route.route("/")
@login_required
def show_categories():
    user_id = session["user_id"]
    transactions = show_all_transactions_from_user(user_id)
    categories = show_all_categories_from_user(user_id)

    return render_template("spend_by_categories.html", categories=categories)


@category_route.route("/all")
@login_required
def show_all_categories():
    user_id = session["user_id"]
    transactions = show_all_transactions_from_user(user_id)
    categories = show_all_categories_from_user(user_id)

    return render_template("categories.html", categories=categories)


@category_route.route("/new", methods=["POST", "GET"])
@login_required
def create_new_category():
    if request.method == "POST":
        user_id = session["user_id"]
        category_name = request.form["category-name"]
        create_new_category_in_db(category_name, user_id)
        return redirect(url_for("category.show_all_categories"))

    return render_template("form_new_category.html")
