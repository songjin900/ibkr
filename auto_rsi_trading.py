from ib_insync import *
import pandas as pd
from indicators.rsi import *
from indicators.stochastic import *
from indicators.macD import *
import sys
from datetime import datetime, timedelta
from playMusic import *
from insertToStock import *
import pytz
from rsi_long_function import *
from rsi_short_function import *

STOCK_NAME = 'TSLA'
STOCK_QUANTITY = 12
BUY_PRICE = 0
RUN_PERCENTAGE = 0.02

RSI_BUY = 33
RSI_SELL = 60

BACK_TO_BACK = True
INITIAL_RUN = True


# rsi only
# buy at 30
# sell at 60

#
util.startLoop()  # uncomment this line when in a notebook
# python3 demo.py
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

account_info = ib.accountValues()
positions = util.df(account_info)
open_positions = ib.positions()

# Convert the open positions data to a DataFrame for easier processing
positions_df = util.df(open_positions)

stock = Stock(STOCK_NAME,'SMART', 'USD')
ticker = ib.reqTickers(stock)[0]  # Get the first ticker object

# Print or manipulate the DataFrame as needed
print("Current Holdings:")
print(positions_df.to_string())


hasPosition = False

loop_count = 0

while True:
    ib.sleep(1)
    try:
        ticker = ib.reqMktData(stock)
        current_price = ticker.marketPrice()
        print("\nCurrent Price:", current_price)

        bars = ib.reqHistoricalData(
            stock, endDateTime='', durationStr='1 D',
            barSizeSetting='1 min', whatToShow='TRADES', useRTH=True)

        loop_count = loop_count + 1
        print(f"loop count: {loop_count}")
        df = util.df(bars)

        current_rsi = rsi(df).iloc[-1].RSI
        print("Current rsi:", current_rsi)
        
        if (current_rsi >= RSI_BUY):
            print("******* Entering LONG POSITION ********")
            rsi_long_function(ib, RUN_PERCENTAGE, STOCK_NAME, STOCK_QUANTITY, RSI_BUY, RSI_SELL, BACK_TO_BACK= False)
        elif (current_rsi >= RSI_SELL):
            print("******* Entering SHORT POSITION ********")
            rsi_short_function(ib, RUN_PERCENTAGE, STOCK_NAME, STOCK_QUANTITY, RSI_BUY, RSI_SELL, BACK_TO_BACK= False)
        else:
            print("no action")
    except Exception as e:
        # Print any exception that occurs
        print(f'An error occurred: {e}')


    
        
          
          
