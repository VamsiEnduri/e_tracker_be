from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os

# ======================================================
# FASTAPI APP
# ======================================================
app = FastAPI()

# ======================================================
# CORS POLICY
# ======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ======================================================
# DATABASE CONNECTION FUNCTION
# ======================================================
def get_db_connection():

    conn = mysql.connector.connect(
        host=os.getenv("db_host"),
        user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        database=os.getenv("db_name"),
        port=int(os.getenv("db_port"))
    )

    return conn

# ======================================================
# CREATE TABLE
# ======================================================
try:

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        expense_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(200),
        amount FLOAT,
        category VARCHAR(100),
        payment_method VARCHAR(100),
        expense_date DATE,
        description TEXT
    )
    """)

    conn.commit()

    cursor.close()
    conn.close()

    print("Table Checked Successfully")

except Exception as e:

    print("DB Error :", e)

# ======================================================
# HOME ROUTE
# ======================================================
@app.get("/")
def home():

    return {
        "message": "Expense Tracker API Running Successfully"
    }

# ======================================================
# ADD EXPENSE
# ======================================================
@app.post("/add_expense")
def add_expense(data: dict):

    try:

        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        INSERT INTO expenses
        (
            title,
            amount,
            category,
            payment_method,
            expense_date,
            description
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            data["title"],
            data["amount"],
            data["category"],
            data["payment_method"],
            data["expense_date"],
            data["description"]
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "message": "Expense Added Successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# ======================================================
# GET ALL EXPENSES
# ======================================================
@app.get("/get_expenses")
def get_expenses():

    try:

        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM expenses
        ORDER BY expense_id DESC
        """

        cursor.execute(query)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            "expenses": data
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# ======================================================
# GET SINGLE EXPENSE
# ======================================================
@app.get("/get_single_expense/{expense_id}")
def get_single_expense(expense_id: int):

    try:

        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM expenses
        WHERE expense_id = %s
        """

        cursor.execute(query, (expense_id,))

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        if data:

            return {
                "expense": data
            }

        return {
            "message": "Expense Not Found"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# ======================================================
# UPDATE EXPENSE
# ======================================================
@app.put("/update_expense/{expense_id}")
def update_expense(expense_id: int, data: dict):

    try:

        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        UPDATE expenses
        SET
            title=%s,
            amount=%s,
            category=%s,
            payment_method=%s,
            expense_date=%s,
            description=%s
        WHERE expense_id=%s
        """

        values = (
            data["title"],
            data["amount"],
            data["category"],
            data["payment_method"],
            data["expense_date"],
            data["description"],
            expense_id
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "message": "Expense Updated Successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# ======================================================
# DELETE EXPENSE
# ======================================================
@app.delete("/delete_expense/{expense_id}")
def delete_expense(expense_id: int):

    try:

        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        DELETE FROM expenses
        WHERE expense_id=%s
        """

        cursor.execute(query, (expense_id,))

        conn.commit()

        cursor.close()
        conn.close()

        return {
            "message": "Expense Deleted Successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# ======================================================
# EXPENSE SUMMARY
# ======================================================
@app.get("/expense_summary")
def expense_summary():

    try:

        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            category,
            SUM(amount) AS total_amount
        FROM expenses
        GROUP BY category
        """

        cursor.execute(query)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            "summary": data
        }

    except Exception as e:

        return {
            "error": str(e)
        }

