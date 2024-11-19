import datetime as dt
import matplotlib as mp
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import mplfinance as mpf
import pandas as pd
import yfinance as yf


style.use("ggplot")

start = dt.datetime(2015,1,1)
end = dt.datetime(2024,12,31)


df = yf.download("NVDA",start, end)
print(df)


df_ohlc = df["Adj Close"].resample("10D").ohlc()
df_volume = df["Volume"].resample("10D").sum()
df_ohlc["volume"] = df_volume
df_ohlc.reset_index(inplace=True)
df_ohlc.columns = ["Date", "open", "high", "low", "close", "volume"]
df_ohlc.set_index("Date", inplace=True)


mpf.plot(df_ohlc,type="candle", title='NVDA', style='charles', ylabel="Price", ylabel_lower="Volume", volume=True)

plt.show()