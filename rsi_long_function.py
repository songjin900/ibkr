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

def rsi_long_function(ib, run_percentage, STOCK_NAME, STOCK_QUANTITY, RSI_BUY, RSI_SELL, BACK_TO_BACK):

    ## this is local variable
    LONG_PRICE = 0
    INITIAL_RUN = True
    
    TOL = 0.05

    # rsi only
    # buy at 30
    # sell at 60

    #
    util.startLoop()  # uncomment this line when in a notebook
    # python3 demo.py
    # ib = IB()
    # ib.connect('127.0.0.1', 7497, clientId=1)

    stock = Stock(STOCK_NAME,'SMART', 'USD')
    ticker = ib.reqTickers(stock)[0]  # Get the first ticker object

    hasPosition = False
    loop_count = 0
    rsiDate = ""

    ##
    # Check if there's a position in Tesla stock
    while True:

        while not hasPosition:
            ib.sleep(1)
            
            try:

                ticker = ib.reqMktData(stock)
                LONG_PRICE = ticker.marketPrice()
                print("\nCurrent Price:", LONG_PRICE)

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


                if (rsiValue > RSI_BUY):
                    continue

                if (rsiValue < previous_rsiValue):
                    continue

                # Get the current time  
                current_time = datetime.now(pytz.utc)
                time_difference = abs(current_time - rsiDate)

                if time_difference <= timedelta(minutes = 1):
                    # Get the current price of the stock
                    LONG_PRICE = ticker.marketPrice()

                    order = ""

                    print("*****************************************Current Price:", round(LONG_PRICE,2))
                    if INITIAL_RUN or not BACK_TO_BACK: 
                        order = LimitOrder('BUY', STOCK_QUANTITY, round(LONG_PRICE,2))  # Buy 100 shares of TSLA at $700 per share
                        saveToDB(current_time, 'Buy', STOCK_NAME, STOCK_QUANTITY, LONG_PRICE, "rsi_longFirst" )
                    elif BACK_TO_BACK:
                        order = LimitOrder('BUY', STOCK_QUANTITY * 2, round(LONG_PRICE,2))  # Buy 100 shares of TSLA at $700 per share
                        saveToDB(current_time, 'Buy Back_To_Back', STOCK_NAME, STOCK_QUANTITY * 2, LONG_PRICE, "rsi_longFirst" )

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

            if rsiValue >= RSI_SELL:
                order = ""

                if BACK_TO_BACK:
                    order = LimitOrder('SELL', STOCK_QUANTITY * 2, round(current_price,2))
                    saveToDB(current_time, 'SELL Back_To_Back', STOCK_NAME, STOCK_QUANTITY*2, current_price, "rsi_longFirst" )
                else:
                    order = LimitOrder('SELL', STOCK_QUANTITY, round(current_price,2))
                    saveToDB(current_time, 'SELL', STOCK_NAME, STOCK_QUANTITY, current_price, "rsi_longFirst" )


                trade = ib.placeOrder(stock, order)

                print ("**** Order Submitted ****")
                tradeStatus = "Submitted"
                while tradeStatus != 'Filled' or tradeStatus != "RUN":
                    print(f"status from IBKR: {trade.orderStatus.status}")
                    if (round(LONG_PRICE,2) * (1 - run_percentage) >= round(current_price,2)):
                        # Cancel all open orders
                        open_orders = ib.openOrders()

                        for order in open_orders:
                            ib.cancelOrder(order)
                        # submit market Order
                        order = MarketOrder('SELL', STOCK_QUANTITY)
                        trade = ib.placeOrder(stock, order)
                        tradeStatus = "RUN"
                        
                    ib.sleep(1)

                print("*************** Order is Filled *************")
                print(f"purchased price: { round(LONG_PRICE,2)}")
                print(f"sold price: { round(current_price,2)}")
                if (round(LONG_PRICE,2) < round(current_price,2)):
                    print("Sold with PROFIT!!!!!!")
                else:
                    print("Sold with LOSS")

                playMusic()
                hasPosition = False 

            elif (round(LONG_PRICE,2) * (1 - run_percentage) >= round(current_price,2)):
                # Fetch all open orders
                open_orders = ib.openOrders()

                # Cancel all open orders
                for order in open_orders:
                    ib.cancelOrder(order)
                
                order = MarketOrder('SELL', STOCK_QUANTITY)
                trade = ib.placeOrder(stock, order)

            else:
                print(f"current price: {round(current_price,2)}")
                print(f"purchased price: { round(LONG_PRICE,2)}")
                print(f"current RSI: {rsiValue}")
                print(f"price to run: {round(LONG_PRICE,2) * (1 - run_percentage)}")
                print("waiting...")
                ib.sleep(1)




        
        



        
            
            
            
