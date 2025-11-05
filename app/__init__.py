from flask import Flask
from app.db import init_db

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize DB when app starts
init_db()
