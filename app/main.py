from flask import render_template, request, redirect, url_for, flash
from app import app   # import app instance from __init__.py
from app.models import get_transactions, add_transaction, delete_transaction

@app.route('/')
def index():
    transactions = get_transactions()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['POST'])
def add():
    date = request.form.get('date')
    description = request.form.get('description')
    category = request.form.get('category')
    type_ = request.form.get('type')
    amount = request.form.get('amount')

    if not (date and description and type_ and amount):
        flash("Please fill in all required fields.")
        return redirect(url_for('index'))

    add_transaction(date, description, category, type_, amount)
    flash("Transaction added successfully!")
    return redirect(url_for('index'))

@app.route('/delete/<int:transaction_id>')
def delete(transaction_id):
    delete_transaction(transaction_id)
    flash("Transaction deleted.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
