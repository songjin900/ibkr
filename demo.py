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


# mode = daily or min
environemnt = 'prod'
mode = 'min'

# util.startLoop()  # uncomment this line when in a notebook
# python3 demo.py
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

account_info = ib.accountValues()
positions = util.df(account_info)

open_positions = ib.positions()

# Convert the open positions data to a DataFrame for easier processing
positions_df = util.df(open_positions)

# Print or manipulate the DataFrame as needed
print("Current Holdings:")
print(positions_df.to_string())
print(positions_df)

# prod: 7497, Dev: 4002
stock = Stock('TSLA','SMART', 'USD')

bars = ib.reqHistoricalData(
    stock, endDateTime='', durationStr='180 D',
    barSizeSetting='1 day', whatToShow='TRADES', useRTH=True)

if (mode == 'min'):
    bars = ib.reqHistoricalData(
        stock, endDateTime='', durationStr='1 D',
        barSizeSetting='1 min', whatToShow='TRADES', useRTH=True)



# convert to pandas dataframe (pandas
# needs to be installed):
df = util.df(bars)

#print (df.to_string())

# sys.exit()

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

##
print(f"stochastic overSold Date: {stochasticOverSoldDate}")
print(f"stochastic overBought Date: {stochasticOverBoughtDate}")

if (stochasticOverSoldDate < stochasticOverBoughtDate ):
    sys.exit()

macDDate = ""

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

if not macDDate:
    sys.exit()

print(f'macDDate is {macDDate}')

rsiDate = ""

if (macDDate):

    for index, row in rsi(df).iterrows():
        date_rsi = row['Date']
        current_rsi = row['RSI']

        if index > 0:
            previous_rsi = rsi(df).iloc[index-1]
            if (date_rsi >= macDDate and current_rsi >= 50):
                rsiDate = date_rsi
                break

print(f"recent date for rsi is {rsiDate}")


# Get the current time
current_time = datetime.now(pytz.utc)

# Check if 'b' is within +- one minute from the current time
time_difference = abs(current_time - rsiDate)

if time_difference <= timedelta(minutes=1):
    print("Time 'b' is within +- one minute from the current time.")
    order = MarketOrder('Buy', 1)
    trade = ib.placeOrder(stock, order)
    print(trade)



# if this rsiDate is within +-1 time.now then buy it. 

# if ()

# order = MarketOrder('Buy', 1)
# trade = ib.placeOrder(stock, order)
# print(trade)











# market_data = ib.reqMktData(stock, '',False,False)

# def onPendingTicker(ticker):
#     print("\npending ticker event received\n")
#     print(ticker)

# ib.pendingTickersEvent += onPendingTicker

# ib.run()
