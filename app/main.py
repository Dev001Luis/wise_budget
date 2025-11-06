from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app   # import app instance from __init__.py
from app.models import get_transactions, get_currencies, add_transaction, delete_transaction


@app.route('/')
def index():
    transactions = get_transactions()
    currencies = get_currencies()
    return render_template('index.html', transactions=transactions, currencies=currencies)


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


@app.route('/chart-data')
def chart_data():
    from app.models import get_monthly_summary
    data = get_monthly_summary()
    return jsonify(data)


@app.route('/expense-breakdown')
def expense_breakdown():
    from app.models import get_expense_breakdown
    return jsonify(get_expense_breakdown())

@app.route('/balance-trend')
def balance_trend():
    from app.models import get_balance_trend
    return jsonify(get_balance_trend())


@app.route('/set-color', methods=['POST'])
def set_color():
    from app.models import insert_category_color
    category = request.form.get("category")
    color = request.form.get("color")
    insert_category_color(category, color)
    flash(f"Color updated for {category}")
    return redirect(url_for('index'))

@app.route("/update-category-colors", methods=["POST"])
def update_category_colors():
    """
    Receives JSON {category: color, ...}, inserts or updates in MySQL.
    """
    from app.models import save_category_colors
    try:
        colors = request.get_json()
        if not colors or not isinstance(colors, dict):
            return jsonify({"error": "Invalid data format"}), 400
        print("passo")

        save_category_colors(colors)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error updating category colors: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/category-colors')
def category_colors():
    from app.models import get_category_colors
    colors = get_category_colors()
    return jsonify(colors)


@app.route("/edit-colors-modal")
def edit_colors_modal():
    from app.models import get_category_colors
    colors = get_category_colors()
    return render_template("modal_edit_colors.html", colors=colors)


if __name__ == '__main__':
    app.run(debug=True)
