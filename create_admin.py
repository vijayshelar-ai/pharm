import mysql.connector
from mysql.connector import connection
import bcrypt

def create_admin_table():
    try:
        conn = connection.MySQLConnection(
            host="localhost",
            user="root",
            password="root",
            database="mydata"
        )
        cursor = conn.cursor()

        # Create admin_login table with email field
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_login (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
        """)
        
        conn.commit()
        print("Admin table created successfully!")
        print("Please create an admin account through the Admin Dashboard")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_admin_table()
