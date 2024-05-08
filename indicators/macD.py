import pandas as pd

def macd(df, short_window=12, long_window=26, signal_window=9):

    prices = list(zip(df.date, df.close))

    # Convert the list of prices into a DataFrame
    data = pd.DataFrame(prices, columns=['Date', 'Close'])
    data['Date'] = pd.to_datetime(data['Date'])

    # Calculate short and long exponential moving averages
    short_ema = data['Close'].ewm(span=short_window, min_periods=1, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, min_periods=1, adjust=False).mean()
    
    # Calculate MACD line
    macd_line = short_ema - long_ema
    
    # Calculate signal line
    signal_line = macd_line.ewm(span=signal_window, min_periods=1, adjust=False).mean()
    
    # Calculate MACD histogram
    macd_histogram = macd_line - signal_line

    # Combine the MACD indicators into a DataFrame
    macd_data = pd.DataFrame({
        'Date': df.date,
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': macd_histogram
    })

    return macd_data
    
    
#    return df.date, macd_line, signal_line, macd_histogram

# # Example list of historical stock prices (list of tuples: date, close)
# # Replace 'your_prices_list' with your actual list of prices
# prices_list = [
#     ('2024-01-01', 50.25),
#     ('2024-01-02', 51.00),
#     # Add more historical prices here
# ]

# # Calculate MACD indicators
# macd_line, signal_line, macd_histogram = calculate_macd(prices_list)

# # Combine the MACD indicators into a DataFrame
# macd_data = pd.DataFrame({
#     'Date': [price[0] for price in prices_list],
#     'MACD': macd_line,
#     'Signal': signal_line,
#     'Histogram': macd_histogram
# })

# # Print the MACD data
# print(macd_data)