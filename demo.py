from ib_insync import *
import pandas as pd
from indicators.rsi import *
from indicators.stochastic import *
from indicators.macD import *
import sys
from datetime import datetime, timedelta
import pytz


# mode = daily or min
environemnt = 'prod'
mode = 'min'



util.startLoop()  # uncomment this line when in a notebook
# python3 demo.py
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

account_info = ib.accountValues()
positions = util.df(account_info)
open_positions = ib.positions()

# Convert the open positions data to a DataFrame for easier processing
positions_df = util.df(open_positions)

# Print or manipulate the DataFrame as needed
# print("Current Holdings:")
# print(positions_df.to_string())
# print(positions_df)

# prod: 7497, Dev: 4002
stock = Stock('TSLA','SMART', 'USD')

print("Time 'b' is within +- one minute from the current time.")
order = MarketOrder('Buy', 1)
trade = ib.placeOrder(stock, order)


# # Define order status handler
# def order_status_handler(order):
#     print("Order status:", order.status)

# # Register the order status handler
# ib.orderStatusEvent += order_status_handler

# Wait for the order to be filled
while trade.orderStatus.status != 'Filled':
    print(trade.orderStatus.status)
    ib.sleep(1)
