import pandas as pd

def rsi(df, window=14):

    data = df.close
    date = df.date

    delta = data.diff()
    
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Smoothing using Wilder's smoothing method
    for i in range(window, len(data)):
        avg_gain[i] = ((window - 1) * avg_gain[i-1] + gain[i]) / window
        avg_loss[i] = ((window - 1) * avg_loss[i-1] + loss[i]) / window
        
        rs[i] = avg_gain[i] / avg_loss[i]
        rsi[i] = 100 - (100 / (1 + rs[i]))
    
    return pd.DataFrame({'Date': date[window:], 'RSI': rsi[window:]})

    # return rsi

