from ib_insync import *
import pandas as pd
from indicators.rsi import *
from indicators.stochastic import *
from indicators.macD import *
import sys
from datetime import datetime, timedelta
from setting.playMusic import *
from DB.insertToStock import *
import pytz
from functions.rsi_long_function import *
from functions.rsi_short_function import *
from functions.writeToText import *


STOCK_QUANTITY = 12
BUY_PRICE = 0
RUN_PERCENTAGE = 0.02

RSI_BUY = 33
RSI_SELL = 60

BACK_TO_BACK = True
INITIAL_RUN = True

index = 0
stocks = ['NVDA','TSLA','ARM','SERV', 'RY','TD','ENB','SHOP','BAM','BN','BMO','CNI','CP','MGA','WCN','MFC','SLF','GIB','OTEX','PBA','TRP','BTG','CCJ','NTR','SU']


# rsi only
# buy at 30
# sell at 60

#
util.startLoop()  # uncomment this line when in a notebook
# python3 demo.py
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)
ib.reqMarketDataType(4)

account_info = ib.accountValues()
positions = util.df(account_info)
open_positions = ib.positions()

# Convert the open positions data to a DataFrame for easier processing
positions_df = util.df(open_positions)

# Print or manipulate the DataFrame as needed
print("Current Holdings:")
print(positions_df.to_string())

hasPosition = False

loop_count = 0

while True:
    ib.sleep(1)
    try:
        stock_name = stocks[index]
        stock = Stock(stock_name,'SMART', 'USD')
        ticker = ib.reqMktData(stock) 

        current_price = ticker.marketPrice()
        print("\nCurrent Price:", current_price)

        bars = ib.reqHistoricalData(
            stock, endDateTime='', durationStr='90 D',
            barSizeSetting='1 Day', whatToShow='TRADES', useRTH=True)
        
        print(stock_name)

        df = util.df(bars)

        current_rsi = rsi(df).iloc[-1].RSI
        print("Current rsi:", current_rsi)
        
        if (current_rsi <= RSI_BUY):
            print("******* Entering LONG POSITION ********")
            write_to_text(stock_name,"RSI",current_rsi,current_price,"buy")
            # rsi_long_function(ib, RUN_PERCENTAGE, stock_name, STOCK_QUANTITY, RSI_BUY, RSI_SELL, BACK_TO_BACK= False)
        elif (current_rsi >= RSI_SELL):
            print("******* Entering SHORT POSITION ********")
            write_to_text(stock_name,"RSI",current_rsi,current_price,"sell")
            # rsi_short_function(ib, RUN_PERCENTAGE, stock_name, STOCK_QUANTITY, RSI_BUY, RSI_SELL, BACK_TO_BACK= False)
        else:
            print(f'{stock_name} - rsi: {current_rsi} - Move to Next Stock')
            write_to_text(stock_name,"RSI",current_rsi,current_price,"Skipped")

        if (index == len(stocks)-1):
            index = 0
            print(index)
        else:
            index = index +1
            print(index)

    except Exception as e:
        # Print any exception that occurs
        print(f'An error occurred: {e}')


    
        
          
          
