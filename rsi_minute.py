
def calculate_rsi(df, period=14):
    gains = []
    losses = []

    rsi_values = []

    prices = df.close

    for i in range(1, len(prices)):
        price_change = prices[i] - prices[i - 1]

        if price_change >= 0:
            gains.append(price_change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(price_change))

        if len(gains) > period:
            gains.pop(0)
            losses.pop(0)

        if len(gains) == period:
            average_gain = sum(gains) / period
            average_loss = sum(losses) / period

            if average_loss == 0:
                rs = 100  # Avoid division by zero
            else:
                rs = average_gain / average_loss

            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)

    return rsi_values

