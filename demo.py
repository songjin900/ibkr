from ib_insync import *
import pandas as pd
from indicators.rsi import *
from indicators.stochastic import *
from indicators.macD import *
import sys
from datetime import datetime, timedelta
import pytz
from insertToStock import *
import sqlite3

# mode = daily or min
environemnt = 'prod'
mode = 'min'

current_time = datetime.now(pytz.utc)
STOCK_NAME = 'TSLA'
STOCK_QUANTITY = 12

SHORT_PRICE = "123.424224"
# saveToDB("2024-05-09", 'SELL Back_To_Back', STOCK_NAME, 12, SHORT_PRICE, "rsi_shortFirst" )

  # Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect('Stock.db')

# Create a cursor object
cursor = conn.cursor()



saveToDB("2024-05-09", 'SELL', STOCK_NAME, 12, SHORT_PRICE, "rsi_shortFirst" )
conn.commit()
# # Query the table
cursor.execute("SELECT * FROM stocks")
print(cursor.fetchall())

# Close the connection
conn.close()
 