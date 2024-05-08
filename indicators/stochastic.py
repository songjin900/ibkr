import pandas as pd
import numpy as np

# if k > d (cross) and both values are below 20 then it is oversold  =  buy
# if k < d (cross) and both values are below 80 then it is overbought = sell. 

def stochastic(df, k_period=14, d_period=3, smoothing=3):

    prices_df = pd.DataFrame({
        'Date': df.date,
        'High': df.high, 
        'Low': df.low,
        'Close': df.close,
        'Open': df.open
    })

    # print(prices_df)

    # Calculate the rolling minimum of lows and rolling maximum of highs

    prices_df['L14'] = prices_df['Low'].rolling(window=k_period).min()
    prices_df['H14'] = prices_df['High'].rolling(window=k_period).max()
    prices_df['%K'] = ((prices_df['Close'] - prices_df['L14']) / (prices_df['H14'] - prices_df['L14'])) * 100.00

  # Calculate %D as a moving average of %K
    prices_df['%D'] = prices_df['%K'].rolling(window=d_period).mean()
    prices_df['%K'] = prices_df['%K'].rolling(window=d_period).mean()

    # Apply smoothing to %D
    prices_df['%D'] = prices_df['%D'].rolling(window=smoothing).mean()
    

    
    return prices_df[['Date', '%K', '%D']]

