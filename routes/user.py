from flask import Blueprint, url_for, request, session, flash, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import register_new_user, check_if_user_is_registered, get_user_full_name, edit_user_profile, get_user_by_id
from decorators import login_required

user_route = Blueprint("user", __name__)


@user_route.route("/register", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        username = request.form["username"]
        fullname = request.form["fullname"]
        password = generate_password_hash(request.form["password"])
        register_new_user(username, fullname, password)
        return redirect(url_for("transaction.index"))
    return render_template("register.html")


@user_route.route("/login", methods=["POST", "GET"])
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
            # PRECISO RETORNAR O INDEX DO TRANSACTIONS
            return redirect(url_for("transaction.index"))
        flash(f"Usuário ou senha inválidos. Tente novamente.", "error")
    return render_template("login.html")


@user_route.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    return redirect(url_for("user.login"))


@user_route.route("/profile")
@login_required
def show_user_profile():
    user_id = session["user_id"]
    full_name = get_user_full_name(user_id)
    return render_template("profile.html", full_name=full_name, user_id=user_id)


@user_route.route("/profile/edit/<int:id>", methods=["POST", "GET"])
@login_required
def edit_profile(id):
    if request.method == "POST":
        user_id = session["user_id"]
        username = request.form["username"]
        fullname = request.form["fullname"]

        edited_profile = edit_user_profile(username, fullname, user_id)
        return redirect(url_for('user.show_user_profile'))

    user = get_user_by_id(id)

    user = {
        "id": user[0],
        "username": user[1],
        "fullname": user[2],
        "password": user[3],
    }

    return render_template("form_edit_user_profile.html", user=user)
