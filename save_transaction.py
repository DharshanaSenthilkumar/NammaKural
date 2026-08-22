import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# SAVE TRANSACTION TO NAMMAKURAL MYSQL
# ============================================================

def save_transaction(transaction):

    connection = None
    cursor = None

    try:

        # ====================================================
        # CONNECT TO DATABASE
        # ====================================================

        connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

        # ====================================================
        # CREATE CURSOR
        # ====================================================

        cursor = connection.cursor()


        # ====================================================
        # SQL INSERT
        # ====================================================

        sql = """
        INSERT INTO transactions
        (type, item, quantity, unit, amount)
        VALUES (%s, %s, %s, %s, %s)
        """


        # ====================================================
        # VALUES
        # ====================================================

        values = (

            transaction.get("type"),

            transaction.get("item"),

            transaction.get("quantity"),

            transaction.get("unit"),

            transaction.get("amount")
        )


        # ====================================================
        # INSERT TRANSACTION
        # ====================================================

        cursor.execute(
            sql,
            values
        )


        # ====================================================
        # COMMIT
        # ====================================================

        connection.commit()


        print(
            "✅ Transaction saved to MySQL!"
        )

        print(
            "Transaction ID:",
            cursor.lastrowid
        )


        return True


    # ========================================================
    # MYSQL ERROR
    # ========================================================

    except mysql.connector.Error as error:

        print(
            "❌ MySQL Error!"
        )

        print(
            error
        )

        return False


    # ========================================================
    # OTHER ERRORS
    # ========================================================

    except Exception as error:

        print(
            "❌ Unexpected error!"
        )

        print(
            error
        )

        return False


    # ========================================================
    # CLOSE CONNECTION
    # ========================================================

    finally:

        if cursor is not None:

            cursor.close()


        if connection is not None:

            connection.close()


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    test_transaction = {

        "type": "expense",

        "item": "rice",

        "quantity": 5,

        "unit": "kg",

        "amount": 250
    }


    print(
        "Testing NammaKural MySQL connection..."
    )


    success = save_transaction(
        test_transaction
    )


    if success:

        print(
            "🎉 Test transaction inserted successfully!"
        )

    else:

        print(
            "⚠️ Test transaction was not inserted."
        )