from flask import Flask
import mysql.connector, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS wisebudget")
cursor.close()
db.close()

if __name__ == "__main__":
    app.run(debug=True)
