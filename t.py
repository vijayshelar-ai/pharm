from mysql.connector import  (connection)
# from mysql.connector import Error

def connect_to_database():
    print("Ongoing connection")
    try:
        # Establish connection to MySQL Workbench
        # connection = mysql.connector.connect(
        #     host="localhost",       # Default host for MySQL Workbench
        #     user="root",            # Replace with your MySQL username
        #     password="root",        # Replace with your MySQL password
        #     database="data"         # Name of the database
        # )
        connections = connection.MySQLConnection(
            host='localhost',
            user='root',
            password='root',
            database='data',
        )
        if connections.is_connected():
            print("Successfully connected to the database 'data'.")

            # Create a cursor object
            cursor = connections.cursor()

            # Query to fetch all data from the 'student' table
            query = "SELECT idstudent FROM student"
            cursor.execute(query)

            # Fetch and print the results
            results = cursor.fetchall()
            print("idstudent values:")
            for row in results:
                print(row[0])  # Access the idstudent column value

            # Close the cursor and connection
            cursor.close()
            connections.close()
        else:
            print("Connection failed.")
    except Error as err:
        print(f"Error: {err}")

# Call the function to connect to the database
connect_to_database()