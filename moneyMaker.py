
from stochastic import *


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


# prod: 7497, Dev: 4002
stock = Stock('TSLA','SMART', 'USD')


bars = ib.reqHistoricalData(
    stock, endDateTime='', durationStr='1 D',
    barSizeSetting='1 min', whatToShow='TRADES', useRTH=True)



# convert to pandas dataframe (pandas
# needs to be installed):
df = util.df(bars)

stochastic(df)
