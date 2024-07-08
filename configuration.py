from flask import Flask, render_template
from routes.category import category_route
from routes.user import user_route
from routes.transaction import transaction_route
from database.database import setup_database


def configure_all(app):
    configure_routes(app)
    configure_database()


def configure_routes(app):
    app.register_blueprint(user_route, url_prefix="/user")
    app.register_blueprint(category_route, url_prefix="/category")
    app.register_blueprint(transaction_route, url_prefix="/")


def configure_database():
    setup_database()
