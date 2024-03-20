import pandas as pd
from ta.momentum import RSIIndicator
from matplotlib import pyplot as plt
from binance import Client

client = Client()
k_lines = client.get_historical_klines(
    symbol="BTCUSDT",
    interval=Client.KLINE_INTERVAL_1MINUTE,
    start_str="1 day ago UTC",
    end_str="now UTC"
)

columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
k_lines_df = pd.DataFrame(k_lines, columns=columns)
k_lines_df[['time', 'open', 'high', 'low', 'close']] = k_lines_df[['time', 'open', 'high', 'low', 'close']].apply(pd.to_numeric, errors='coerce')
k_lines_df['time'] = pd.to_datetime(k_lines_df['time'], unit='ms')

periods = [14, 27, 100]
for period in periods:
    k_lines_df[f'RSI_{period}'] = RSIIndicator(k_lines_df['close'], period).rsi()

plt.figure(figsize=(14, 10))
plt.subplot(len(periods) + 1, 1, 1)
plt.plot(k_lines_df['time'], k_lines_df['close'], label='Close Price')
plt.title('Close Price')
plt.legend()

for i, period in enumerate(periods, start=2):
    plt.subplot(len(periods) + 1, 1, i)
    plt.plot(k_lines_df['time'], k_lines_df[f'RSI_{period}'], label=f'RSI_{period}')
    plt.title(f'RSI_{period}')
    plt.legend()

plt.tight_layout()
plt.show()
