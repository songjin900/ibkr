from ib_insync import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from indicators.stochastic import *
from indicators.macD import *
from datetime import datetime
import pytz
from setting.playMusic import *

showMessage = True

async def stochastic_buy_function(stock, ib):
    ib.sleep(5)

    stock_contract = Stock(stock, 'SMART', 'USD')

    print("getting data")
    bars = await ib.reqHistoricalDataAsync(
        stock_contract, endDateTime='', durationStr='1 D',
        barSizeSetting='15 mins', whatToShow='TRADES', useRTH=False)

    df = util.df(bars)

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
        return

    stochasticOverSoldDate = datetime.strptime(str(stochasticOverSoldDate), "%Y-%m-%d %H:%M:%S%z")

    if (stochasticOverBoughtDate):
        stochasticOverBoughtDate = datetime.strptime(str(stochasticOverBoughtDate), "%Y-%m-%d %H:%M:%S%z")

    if (stochasticOverBoughtDate and (stochasticOverSoldDate < stochasticOverBoughtDate) ):
        return
    else:
        return stochasticOverSoldDate
