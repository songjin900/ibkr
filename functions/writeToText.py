import os
from datetime import datetime, timezone
import pytz

def write_to_text(stockName, indicator, indicatorNumber, currentPrice, action):
    filename = "DailyBuyList.txt"
    dt = datetime.now(timezone.utc)
    with open(filename, "a") as file:
        file.write(f'\n{dt} - {action} {stockName} at ${currentPrice}. {indicator} is at {indicatorNumber}')