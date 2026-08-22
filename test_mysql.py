import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
try:
    connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

    print("✅ Connected to MySQL!")
    print("Database:", connection.database)

    connection.close()

except mysql.connector.Error as error:
    print("❌ Connection failed!")
    print(error)