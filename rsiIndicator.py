from ib_insync import *
import pandas as pd
from indicators.rsi import *
from indicators.stochastic import *
from indicators.macD import *
import sys
from datetime import datetime, timedelta
from playMusic import *
import pytz

STOCK_NAME = 'TSLA'
STOCK_QUANTITY = 13
BUY_PRICE = 0

RSI_BUY = 30
RSI_SELL = 50

BACK_TO_BACK = False
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
macDDate = ""
rsiDate = ""

##
# Check if there's a position in Tesla stock
while True:

    while not hasPosition:
        ib.sleep(1)
        
        try:

            ticker = ib.reqMktData(stock)
            BUY_PRICE = ticker.marketPrice()
            print("\nCurrent Price:", BUY_PRICE)

            bars = ib.reqHistoricalData(
                stock, endDateTime='', durationStr='1 D',
                barSizeSetting='1 min', whatToShow='TRADES', useRTH=True)

            loop_count = loop_count + 1
            print(f"loop count: {loop_count}")
            df = util.df(bars)

            current_rsi = rsi(df).iloc[-1]
     
            rsiDate = current_rsi.Date
            rsiValue = current_rsi.RSI

            print(f"current rsi is {rsiValue}")
            if (rsiValue > RSI_BUY):
                continue

            # Get the current time  
            current_time = datetime.now(pytz.utc)
            time_difference = abs(current_time - rsiDate)

            if time_difference <= timedelta(minutes = 1):
                # Get the current price of the stock
                BUY_PRICE = ticker.marketPrice()

                order = ""

                print("*****************************************Current Price:", round(BUY_PRICE,2))
                if INITIAL_RUN or not BACK_TO_BACK: 
                    order = LimitOrder('BUY', STOCK_QUANTITY, round(BUY_PRICE,2))  # Buy 100 shares of TSLA at $700 per share
                elif BACK_TO_BACK:
                    order = LimitOrder('BUY', STOCK_QUANTITY * 2, round(BUY_PRICE,2))  # Buy 100 shares of TSLA at $700 per share

                # Place the order
                trade = ib.placeOrder(stock, order)
                INITIAL_RUN = False

                while trade.orderStatus.status != 'Filled':
                    print(trade.orderStatus.status)
                    ib.sleep(1)
        
                print("*************** Order is Filled *************")
                playMusic()
                hasPosition = True
            else:
                print("Time 'rsi' is not in +- one min time frame.")
                continue

        except:
            continue

    while hasPosition: 
        current_rsi = rsi(df).iloc[-1]
        rsiDate = current_rsi.Date
        rsiValue = current_rsi.RSI
        current_price = ticker.marketPrice()

        if rsiValue >= RSI_SELL:
            order = ""

            if BACK_TO_BACK:
                order = LimitOrder('SELL', STOCK_QUANTITY * 2, round(current_price,2))
            else:
                order = LimitOrder('SELL', STOCK_QUANTITY, round(current_price,2))

            trade = ib.placeOrder(stock, order)

            print ("**** Order Submitted ****")
            while trade.orderStatus.status != 'Filled':
                print(trade.orderStatus.status)
                ib.sleep(1)

            print("*************** Order is Filled *************")
            print(f"purchased price: { round(BUY_PRICE,2)}")
            print(f"sold price: { round(current_price,2)}")
            if (round(BUY_PRICE,2) < round(current_price,2)):
                print("Sold with PROFIT!!!!!!")
            else:
                print("Sold with LOSS")

            playMusic()
            hasPosition = False 
        else:
            print(f"current price: {round(current_price,2)}")
            print(f"purchased price: { round(BUY_PRICE,2)}")
            print(f"current RSI: {rsiValue}")
            print("waiting...")
            ib.sleep(1)




    
    



    
        
          
          
