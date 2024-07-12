import os
import ccxt
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Initialize the exchange (Binance for this example)
exchange = ccxt.binance()

def fetch_ohlcv(symbol, timeframe, since):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
    data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    return data

def plot_chart(data, title, filename):
    plt.figure(figsize=(10, 5))
    plt.plot(data['timestamp'], data['close'], label='Close Price', color='b', marker='o')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def get_timeframes():
    now = datetime.now()
    return {
        '1d': (exchange.parse8601((now - timedelta(days=1)).isoformat()), '1m'),
        '1w': (exchange.parse8601((now - timedelta(weeks=1)).isoformat()), '15m'),
        '1m': (exchange.parse8601((now - timedelta(days=30)).isoformat()), '1h'),
        '1y': (exchange.parse8601((now - timedelta(days=365)).isoformat()), '1d')
    }

def fetch_and_plot(symbol):
    timeframes = get_timeframes()
    for period, (since, timeframe) in timeframes.items():
        data = fetch_ohlcv(symbol, timeframe, since)
        directory = os.path.join('D:\\Internship', symbol.replace('/', '_'))
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, f"{symbol.replace('/', '_')}_{period}.png")
        plot_chart(data, f"{symbol} - Last {period.upper()}", filename)
        csv_filename = os.path.join(directory, f"{symbol.replace('/', '_')}_{period}.csv")
        data.to_csv(csv_filename, index=False)
        print(f"Chart and data for {symbol} ({period}) saved as {filename} and {csv_filename}")

def main():
    crypto_assets = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    for asset in crypto_assets:
        fetch_and_plot(asset)

if __name__ == "__main__":
    main()
