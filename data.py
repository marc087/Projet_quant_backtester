import yfinance as yf

df = yf.download("AAPL", start="2020-01-01", end="2024-01-01")
df.columns = df.columns.get_level_values("Price")  # on jette le niveau Ticker