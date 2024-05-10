import sqlite3

# Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect('Stock.db')

# Create a cursor object
cursor = conn.cursor()

cursor.execute('drop table stocks')

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
             (date text, trans text, symbol text, qty real, price real, file text)''')
cursor.execute(f"INSERT INTO stocks VALUES ('2024-01-01', 'example', 'tsla', 44, 22, 'demo')")

# Save (commit) the changes
conn.commit()

cursor.execute("SELECT * FROM stocks")
print(cursor.fetchall())

# Close the connection
conn.close()
