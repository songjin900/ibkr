from ib_insync import *
import pandas as pd
import threading
from run_function import *
import asyncio

stocks = ["TSLA","NVDA"]

async def main():

    try: 
        # Make a connection or start
        util.startLoop()
        ib = IB()
        await ib.connectAsync('127.0.0.1', 7497, clientId=1)

        open_positions = ib.positions()
        positions_df = util.df(open_positions)
        print(f"Current Holdings:")
        # print(positions_df.to_string())

        # aapl_positions = positions_df[positions_df['contract'].apply(lambda x: x.symbol) == 'NVDL']

        # if not aapl_positions.empty:
        #     total_aapl = aapl_positions['position'].sum()
        #     print(f"Total AAPL stocks: {total_aapl}")
        # else:
        #     print("No AAPL stocks found in open positions.")
        



        ##Run tasks concurrently
        tasks = [run(i + 1, stock, ib) for i, stock in enumerate(stocks)]
        await asyncio.gather(*tasks)
    finally:
        ib.disconnect()

    print("All tasks have finished execution.")

if __name__ == "__main__":
    asyncio.run(main())