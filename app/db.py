import mysql.connector, os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@contextmanager
def get_cursor(dictionary=False):
    db = get_db_connection()
    cursor = db.cursor(dictionary=dictionary)
    try:
        yield cursor
        db.commit()
    finally:
        cursor.close()
        db.close()

def init_db():
    create_table_transaction_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            description VARCHAR(255) NOT NULL,
            category VARCHAR(100),
            type ENUM('Income', 'Expense') NOT NULL,
            currency VARCHAR(10) default '£',
            amount DECIMAL(10,2) NOT NULL
        );
    """

    create_table_category_colors_query = """
        CREATE TABLE IF NOT EXISTS category_colors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(100) UNIQUE NOT NULL,
            color VARCHAR(20) NOT NULL
        );
    """

    with get_cursor() as cursor:
        cursor.execute(create_table_transaction_query)
        cursor.execute(create_table_category_colors_query)

