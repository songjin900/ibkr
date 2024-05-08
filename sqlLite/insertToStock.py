import sqlite3

def saveToDB(date, trans, symbol, qty, price, file):

    try: 

        # Connect to database (or create it if it doesn't exist)
        conn = sqlite3.connect('Stock.db')

        # Create a cursor object
        cursor = conn.cursor()

        # Insert data into the table
        cursor.execute(f"INSERT INTO stocks VALUES ({date}, {trans}, {symbol}, {qty}, {price}, {file})")

        # Save (commit) the changes
        conn.commit()

        # Query the table
        cursor.execute("SELECT * FROM stocks")
        print(cursor.fetchall())

        # Close the connection
        conn.close()
    except:
        print("error in sqlLite")
