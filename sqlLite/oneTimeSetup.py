import sqlite3

# Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect('Stock.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
             (date text, trans text, symbol text, qty real, price real, file text)''')

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()
