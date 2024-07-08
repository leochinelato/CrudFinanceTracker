from flask import Flask
from configuration import configure_all
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET KEY", os.urandom(12).hex())

configure_all(app)

app.run(port=8000, debug=True)
