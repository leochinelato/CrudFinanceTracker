from functools import wraps
from flask import redirect, url_for, request, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function
