from ib_insync import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from indicators.stochastic import *
from indicators.macD import *
from datetime import datetime, timedelta
import pytz
from playMusic import *
from multithreading.stochastic_buy import *
from multithreading.stochastic_sell import *

showMessage = True
Back_To_Back = False
INITIAL_RUN = True
STOCK_QUANTITY = 10
HAS_POSITION = False

async def run(thread_id, stock, ib):

    while True:
        # ib.sleep(15)
        print(f"stock name: {stock}")

        open_positions = ib.positions()

        # Convert the open positions data to a DataFrame for easier processing
        # positions_df = util.df(open_positions)
        # # Print or manipulate the DataFrame as needed
        # print(f"Current Holdings:  Thread: {thread_id}")
        # print(positions_df.to_string())

        stochastic_buy_Loop = True
        stochastic_buy_Date = ""
        while stochastic_buy_Loop:
            stochastic_buy_Date = await stochastic_buy_function(stock, ib)
            if (stochastic_buy_Date is not None): 
                stochastic_buy_Loop = False

        stock_contract = Stock(stock,'SMART', 'USD')
        ticker = ib.reqTickers(stock_contract)[0]  # Get the first ticker object

        # Get the current time  
        current_time = datetime.now(pytz.utc)
        time_difference = abs(current_time - stochastic_buy_Date)

        if time_difference <= timedelta(minutes = 1):
            # Get the current price of the stock
            BUY_PRICE = ticker.marketPrice()

            print("*****************************************Current Price:", round(BUY_PRICE,2))
            order = LimitOrder('BUY', STOCK_QUANTITY, round(BUY_PRICE,2))  # Buy 100 shares of TSLA at $700 per share

            # Place the order
            trade = ib.placeOrder(stock, order)

            while trade.orderStatus.status != 'Filled':
                print(trade.orderStatus.status)
                ib.sleep(1)
        
            print("*************** Order is Filled *************")
            HAS_POSITION = True
            playMusic()

            # SELL PROCESS
            ## here I need a loss stopper or gain stopper
            while (HAS_POSITION):

                stochastic_sell_Loop = True
                stochastic_sell_Date = ""
                while stochastic_sell_Loop:
                    stochastic_sell_Date = await stochastic_sell_function(stock, ib)
                    if (stochastic_sell_Date is not None): 
                        stochastic_sell_Loop = False

                  # Get the current time  
                current_time = datetime.now(pytz.utc)
                time_difference = abs(current_time - stochastic_buy_Date)

                if time_difference <= timedelta(minutes = 1):
                # Get the current price of the stock
                    SELL_PRICE = ticker.marketPrice()
                    order = LimitOrder('SELL', STOCK_QUANTITY, round(SELL_PRICE,2))
                    trade = ib.placeOrder(stock, order)
                    
                    while trade.orderStatus.status != 'Filled':
                        print(trade.orderStatus.status)
                        ib.sleep(1)

                    print("*************** Order is Filled *************")
                    playMusic()
                    HAS_POSITION = False 

                    if (BUY_PRICE <= SELL_PRICE):
                        print ("**** Order Submitted with PROFIT ****")
                    else:
                        print ("**** Order Submitted with PROFIT ****")


        else:
            print("time diff")
            print(time_difference)

        print("done in run_function")

