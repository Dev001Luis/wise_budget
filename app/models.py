from app.db import get_cursor


def get_transactions(limit=25):
    with get_cursor(dictionary=True) as cursor:
        query = "SELECT * FROM transactions ORDER BY date DESC LIMIT %s"
        cursor.execute(query, (limit,))
        result = cursor.fetchall()
        return result if result else []


def add_transaction(date, description, category, type, amount):
    with get_cursor() as cursor:
        query = """
            INSERT INTO transactions (date, description, category, type, amount)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (date, description, category, type, amount))


def delete_transaction(transaction_id):
    with get_cursor() as cursor:
        query = "DELETE FROM transactions WHERE id = %s"
        cursor.execute(query, (transaction_id,))


# 11/05/2025 Add montly summary
def get_monthly_summary():
    with get_cursor(dictionary=True) as cursor:
        query = """
            SELECT  DATE_FORMAT(date, '%Y-%m') AS month,
                    SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) AS total_income,
                    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS total_expense
            FROM    transactions
            GROUP BY month
            ORDER BY month ASC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result or []


def get_expense_breakdown():
    with get_cursor(dictionary=True) as cursor:
        query = """
            SELECT  category, 
                    SUM(amount) AS total
            FROM    transactions
            WHERE   type = 'Expense'
            GROUP BY category
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result or []


def get_balance_trend():
    with get_cursor(dictionary=True) as cursor:
        query = """
            SELECT  DATE_FORMAT(date, '%Y-%m-%d') AS day,
                    SUM(CASE WHEN type = 'Income' THEN amount ELSE -amount END) 
                    OVER (ORDER BY date) AS balance
            FROM    transactions
            ORDER BY date ASC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result or []
