from flask import Flask, render_template, request, redirect, url_for, flash
from app import db

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize DB (once at startup)
db.init_db()

@app.route('/')
def index():    
    transactions = db.db_get_transactions()
    return render_template('index.html', transactions=transactions)
