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

STOCK_NAME = 'TSLA'
STOCK_QUANTITY = 12
SHORT_PRICE = 0

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
macDDate = ""
rsiDate = ""

##
# Check if there's a position in Tesla stock
while True:

    while not hasPosition:
        ib.sleep(1)
        
        try:
            ticker = ib.reqMktData(stock)
            SHORT_PRICE = ticker.marketPrice()
            print("\nCurrent Price:", SHORT_PRICE)

            bars = ib.reqHistoricalData(
                stock, endDateTime='', durationStr='1 D',
                barSizeSetting='1 min', whatToShow='TRADES', useRTH=True)

            loop_count = loop_count + 1
            print(f"loop count: {loop_count}")
            df = util.df(bars)

            current_rsi = rsi(df).iloc[-1]
            previous_rsi = rsi(df).iloc[-2]

            rsiDate = current_rsi.Date
            rsiValue = current_rsi.RSI
            previous_rsiValue = previous_rsi.RSI

            print(f"current rsi is {rsiValue}")
            print(f"previous rsi is {previous_rsiValue}")

            if (rsiValue < RSI_SELL):
                continue

            if (rsiValue > previous_rsiValue):
                continue

            # Get the current time  
            current_time = datetime.now(pytz.utc)
            time_difference = abs(current_time - rsiDate)

            if time_difference <= timedelta(minutes = 1):
                # Get the current price of the stock
                SHORT_PRICE = ticker.marketPrice()

                order = ""

                print("*****************************************Current Price:", round(SHORT_PRICE,2))
                if INITIAL_RUN or not BACK_TO_BACK: 
                    order = LimitOrder('SELL', STOCK_QUANTITY, round(SHORT_PRICE,2))  # Buy 100 shares of TSLA at $700 per share
                    saveToDB(current_time, 'SELL', STOCK_NAME, STOCK_QUANTITY, SHORT_PRICE, "rsi_shortFirst" )
                elif BACK_TO_BACK:
                    order = LimitOrder('SELL', STOCK_QUANTITY * 2, round(SHORT_PRICE,2))  # Buy 100 shares of TSLA at $700 per share
                    saveToDB(current_time, 'SELL Back_To_Back', STOCK_NAME, STOCK_QUANTITY * 2, SHORT_PRICE, "rsi_shortFirst" )

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

        bars = ib.reqHistoricalData(
        stock, endDateTime='', durationStr='1 D',
        barSizeSetting='1 min', whatToShow='TRADES', useRTH=True)

        df = util.df(bars)
        current_rsi = rsi(df).iloc[-1]
        rsiDate = current_rsi.Date
        rsiValue = current_rsi.RSI
        current_price = ticker.marketPrice()

        if rsiValue <= RSI_BUY:
            order = ""

            if BACK_TO_BACK:
                order = LimitOrder('BUY', STOCK_QUANTITY * 2, round(current_price,2))
                saveToDB(current_time, 'BUY Back_To_Back', STOCK_NAME, STOCK_QUANTITY*2, current_price, "rsi_shortFirst" )
            else:
                order = LimitOrder('BUY', STOCK_QUANTITY, round(current_price,2))
                saveToDB(current_time, 'BUY', STOCK_NAME, STOCK_QUANTITY, current_price, "rsi_shortFirst" )


            trade = ib.placeOrder(stock, order)

            print ("**** Order Submitted ****")
            while trade.orderStatus.status != 'Filled':
                print(trade.orderStatus.status)
                ib.sleep(1)

            print("*************** Order is Filled *************")
            print(f"sold(short) price: { round(SHORT_PRICE,2)}")
            print(f"purchase(long) price: { round(current_price,2)}")

            if (round(SHORT_PRICE,2) > round(current_price,2)):
                print("Sold with PROFIT!!!!!!")
            else:
                print("Sold with LOSS")

            playMusic()
            hasPosition = False 
        else:
            print(f"current price: {round(current_price,2)}")
            print(f"purchased price: { round(SHORT_PRICE,2)}")
            print(f"current RSI: {rsiValue}")
            print("waiting...")
            ib.sleep(1)




    
    



    
        
          
          
