from ib_insync import *
import pandas as pd
from rsi import *
from stochastic import *
from macD import *
import sys
from rsi_minute import *
from truncateDate import *
from datetime import datetime, timedelta
import pytz

STOCK_NAME = 'TSLA'
STOCK_QUANTITY = 8
BUY_PRICE = 0
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

        [dateStochastic, k, d] = stochastic(df)

        stochasticOverSoldDate = ""
        stochasticOverBoughtDate = ""

        for index, row in stochastic(df).iterrows():
            date = row['Date']
            percent_k = row['%K']
            percent_d = row['%D']

            if (index > 0):
                previous_row = stochastic(df).iloc[index - 1]
                previous_k = previous_row['%K']
                previous_d = previous_row['%D']

                if (previous_k < previous_d and percent_k > percent_d and percent_k < 20 and percent_d < 20):
                            stochasticOverSoldDate = date

                if (previous_k > previous_d and percent_k < percent_d and percent_k > 80 and percent_d > 80):
                            stochasticOverBoughtDate = date

        ## Initial condition
        print(f"stochastic overSold Date: {stochasticOverSoldDate}")
        print(f"stochastic overBought Date: {stochasticOverBoughtDate}")

        if (not stochasticOverSoldDate):
            print(f"stochasticOverSoldDate is NAN")
            continue

        stochasticOverSoldDate = datetime.strptime(str(stochasticOverSoldDate), "%Y-%m-%d %H:%M:%S%z")

        if (stochasticOverBoughtDate):
            stochasticOverBoughtDate = datetime.strptime(str(stochasticOverBoughtDate), "%Y-%m-%d %H:%M:%S%z")

        if (stochasticOverBoughtDate and (stochasticOverSoldDate < stochasticOverBoughtDate) ):
            continue

        for index, row in macd(df).iterrows():
            macD_date = row['Date']
            macDLine = row['MACD']
            signal = row['Signal']

            if index > 0:
                previous_row = macd(df).iloc[index - 1]
                previous_macd = previous_row['MACD']
                previous_signal = previous_row['Signal']

            if macD_date >= stochasticOverSoldDate and macDLine > signal and previous_macd < previous_signal:
                macDDate = macD_date
                break

        if (not macDDate):
            print(f'no macD signal')
            continue

        print(f'macD date: {macDDate}')

        # for index, row in rsi(df).iterrows():
        #     date_rsi = row['Date']
        #     current_rsi = row['RSI']

        #     if index > 0 and rsi(df):
        #         previous_rsi = rsi(df).iloc[index - 1]
        #         if (date_rsi >= macDDate and current_rsi >= 50):
        #             rsiDate = date_rsi
        #             break

        # for index, row in rsi_df.iterrows():
        #     date_rsi = row['Date']
        #     current_rsi = row['RSI']

        #     if index > 0:
                
        #         # previous_rsi = rsi_df.iloc[index - 1]['RSI']  # Assuming you want the previous RSI value
        #         if date_rsi >= macDDate and current_rsi >= 50:
        #             rsiDate = date_rsi
        #             break
        
        previous_rsi = None

        rsi_df = rsi(df)

        for index, row in rsi_df.iterrows():
            date_rsi = row['Date']
            current_rsi = row['RSI']

            # Skip the first row because there's no previous RSI value
            if previous_rsi is not None:
                if date_rsi >= macDDate and current_rsi >= 50 and current_rsi > previous_rsi:
                    rsiDate = date_rsi
                    break

            # Update previous_rsi for the next iteration
            previous_rsi = current_rsi
        
        if (not rsiDate):
            print(f'no rsi signal')
            print(f"currnet rsi: {current_rsi}")
            continue

        print(f"rsi date: {rsiDate}")

        # Get the current time  
        current_time = datetime.now(pytz.utc)
        time_difference = abs(current_time - rsiDate)

        if time_difference <= timedelta(minutes=1):
            print("Time 'rsi' is within +- one minute from the current time.")

            # Get the current price of the stock
            BUY_PRICE = ticker.marketPrice()

            print("*****************************************Current Price:", round(BUY_PRICE,2))
            # Create a limit order
            order = LimitOrder('BUY', STOCK_QUANTITY, round(BUY_PRICE,2))  # Buy 100 shares of TSLA at $700 per share

            # Place the order
            orderId = ib.placeOrder(stock, order)

            # order = MarketOrder('Buy', 1)
            # trade = ib.placeOrder(stock, order)
            # print(trade)
            hasPosition = True
        else:
            print("Time 'rsi' is not in +- one min time frame.")
            continue

    except:
         continue

while hasPosition: 
    open_positions = ib.positions()
    for position in open_positions:
        print(position.contract.symbol)
        print(STOCK_NAME)
        print(positions_df.to_string())

        if (position.contract.symbol == STOCK_NAME):
            print("submitting orders")
            order = LimitOrder('SELL', STOCK_QUANTITY, BUY_PRICE * 1.005)
            orderId = ib.placeOrder(stock, order)
            hasPosition = False 



    
        
          
          
