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


# def get_category_colors():
#     with get_cursor(dictionary=True) as cursor:
#         query = ("SELECT category, color FROM category_colors")
#         cursor.execute(query)
#         results = cursor.fetchall()
#         return {row["category"]: row["color"] for row in results}

# def set_category_color(category, color):
#     with get_cursor() as cursor:
#         query = """
#             INSERT INTO category_colors (category, color)
#             VALUES (%s, %s)
#             ON DUPLICATE KEY UPDATE color = VALUES(color)
#         """
#         cursor.execute(query, (category, color))

def get_category_colors():
    """
    Fetch all categories and their assigned colors.
    Returns: { 'Food': '#FF5733', 'Bills': '#33A1FF' }
    """
    with get_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT category, color FROM category_colors")
        rows = cursor.fetchall()
        return {row["category"]: row["color"] for row in rows} if rows else {}


def insert_category_color(category: str, color: str):
    """Insert a new category-color pair into the table."""
    with get_cursor(dictionary=True) as cursor:
        cursor.execute("""
            INSERT INTO category_colors (category, color)
            VALUES (%s, %s)
        """, (category, color))


def update_category_color(category: str, color: str):
    """Update color for an existing category."""
    with get_cursor(dictionary=True) as cursor:
        cursor.execute("""
            UPDATE category_colors
            SET color = %s
            WHERE category = %s
        """, (color, category))


def category_exists(category: str) -> bool:
    """Check if a category already exists in the category_colors table."""
    with get_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM category_colors WHERE category = %s", (category,))
        result = cursor.fetchone()
        return result["count"] > 0


def save_category_colors(colors: dict):
    """
    Receives a dictionary {category: color, ...}
    Updates existing rows or inserts new ones.
    """
    if not colors:
        return

    for category, color in colors.items():
        if category_exists(category):
            update_category_color(category, color)
        else:
            insert_category_color(category, color)
