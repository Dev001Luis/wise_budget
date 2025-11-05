from app.db import get_cursor

def get_transactions(limit=25):
    with get_cursor(dictionary=True) as cursor:
        query = "SELECT * FROM transactions ORDER BY date DESC LIMIT %s", (limit,)
        cursor.execute(query)
        result = cursor.fetchall()
        return result if result else None

def add_transaction(date, description, category, type, amount):
    with get_cursor() as cursor:
        query = ("""
            INSERT INTO transactions (date, description, category, type, amount)
            VALUES (%s, %s, %s, %s, %s)
        """, (date, description, category, type, amount))
        cursor.execute(query)
        return "yay"

def delete_transaction(transaction_id):
    with get_cursor() as cursor:
        query = "DELETE FROM transactions WHERE id = %s", (transaction_id,)
        cursor.execute(query)
