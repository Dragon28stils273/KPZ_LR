import pandas as pd
from binance.client import Client

def get_historical_data(symbol, start_str, end_str):
    client = Client()
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, start_str, end_str)
    data = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data = data[['time', 'open', 'high', 'low', 'close', 'volume']]
    data['time'] = pd.to_datetime(data['time'], unit='ms')
    for column in ['open', 'high', 'low', 'close', 'volume']:
        data[column] = pd.to_numeric(data[column], errors='coerce')
    return data

def calculate_RSI(df, periods):
    delta = df['close'].diff()
    loss = delta.where(delta < 0, 0).abs()
    gain = delta.where(delta > 0, 0)

    rsi_frames = pd.DataFrame()
    rsi_frames['time'] = df['time']

    for period in periods:
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_frames[f'RSI {period}'] = rsi

    return rsi_frames

# Example Usage:
symbol = 'BTCUSDT'
yesterday = pd.Timestamp.now() - pd.Timedelta(days=1)
start_str = yesterday.strftime('%Y-%m-%d 00:00')
end_str = (yesterday + pd.Timedelta(days=1)).strftime('%Y-%m-%d 00:00')

data = get_historical_data(symbol, start_str, end_str)
rsi_data = calculate_RSI(data, [14, 27, 100])

print(rsi_data)
