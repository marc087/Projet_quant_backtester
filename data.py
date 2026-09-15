import yfinance as yf
import pandas as pd

def load_ohlcv(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end)
    df.columns = df.columns.get_level_values("Price")  # on jette le niveau Ticker
    return df