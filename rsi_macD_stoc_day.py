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
GAIN = 0.003
LOSS = 0.003
GAINSIG = 0.002
LOSSSIG = 0.002


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

account_info = ib.accountValues()
positions = util.df(account_info)
open_positions = ib.positions()

# Convert the open positions data to a DataFrame for easier processing
positions_df = util.df(open_positions)


stocks = ["TSLA","NVDA","INTC","AMD","QCOM","AAPL","AMZN","GOOGL"]


# Print or manipulate the DataFrame as needed
print("Current Holdings:")
print(positions_df.to_string())

showMessage = False
macDDate = ""
rsiDate = ""

for s in stocks: 

    stock = Stock(s,'SMART', 'USD')
    ticker = ib.reqTickers(stock)[0]  # Get the first ticker object

    BUY_PRICE = ticker.marketPrice()
    if showMessage:
        print("\nCurrent Price:", BUY_PRICE)

    bars = ib.reqHistoricalData(
        stock, endDateTime='', durationStr='90 D',
        barSizeSetting='1 Day', whatToShow='TRADES', useRTH=True)

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

            if (previous_k > previous_d and percent_k < percent_d and percent_k > 75 and percent_d > 75):
                        stochasticOverBoughtDate = date

    ## Initial condition
    if showMessage:
        print(f"stochastic overSold Date: {stochasticOverSoldDate}")
        print(f"stochastic overBought Date: {stochasticOverBoughtDate}")

    if (not stochasticOverSoldDate):
        if showMessage:
             print(f"stochasticOverSoldDate is NAN")
        continue

    stochasticOverSoldDate = datetime.strptime(str(stochasticOverSoldDate), "%Y-%m-%d")

    if (stochasticOverBoughtDate):
        stochasticOverBoughtDate = datetime.strptime(str(stochasticOverBoughtDate), "%Y-%m-%d")

    if (stochasticOverBoughtDate and (stochasticOverSoldDate < stochasticOverBoughtDate) ):
        continue

    for index, row in macd(df).iterrows():
        macD_date = datetime.strptime(str(row['Date']), "%Y-%m-%d").date()
        macDLine = row['MACD']
        signal = row['Signal']

        if index > 0:
            previous_row = macd(df).iloc[index - 1]
            previous_macd = previous_row['MACD']
            previous_signal = previous_row['Signal']

        if macD_date >= stochasticOverSoldDate.date() and macDLine > signal and previous_macd < previous_signal:
            macDDate = macD_date
            break

    if (not macDDate):
        if showMessage:
            print(f'no macD signal')
        continue

    if showMessage:
        print("macd Date date")
        print(f'macD date: {macDDate}')

    previous_rsi = None

    rsi_df = rsi(df)

    for index, row in rsi_df.iterrows():
        date_rsi = datetime.strptime(str(row['Date']), "%Y-%m-%d").date()
        current_rsi = row['RSI']

        # Skip the first row because there's no previous RSI value
        if previous_rsi is not None:
            if date_rsi >= macDDate and current_rsi >= 50 and current_rsi > previous_rsi:
                rsiDate = date_rsi
                break

        # Update previous_rsi for the next iteration
        previous_rsi = current_rsi
    
    if (not rsiDate):
        if showMessage:
            print(f'no rsi signal')
            print(f"currnet rsi: {current_rsi}")
        continue


    print()
    print(f"stock name: {s}")
    print(f"rsi date: {rsiDate}")
    print(f"rsi value: {current_rsi}")



  

     

