import numpy as np 
import yfinance as yf

N = 60 # 2 mois, court terme à comparer plus tard avec 252 (jours de bourse en 1 an)

df = yf.download("AAPL", start="2020-01-01", end="2024-01-01")
df.columns = df.columns.get_level_values("Price")  # on jette le niveau Ticker

def perf_N(close):
    return close.pct_change(periods=N)

def Signal_Momentum(rendement):
    return np.where(rendement.isna(), 0, (rendement > 0).astype(int))

def Cum_Return_Momentum(df):
    df["Return"] = df["Close"].pct_change()   # rendement journalier
    df["perf_N"] = perf_N(df["Close"])
    df["Signal"] = Signal_Momentum(df["perf_N"])
    # puis on applique le signal au rendement
    df["Return_Momentum"] = df["Signal"].shift(1) * df["Return"] # rendement de la stratégie
    # on multiplie successivement les rendements
    df["CumReturn_Momentum"] = (1 + df["Return_Momentum"]).cumprod() # rendement cumulé

def main():
    Cum_Return_Momentum(df)
    print(df[len(df)-6:].head())

if __name__ == "__main__":
    main()

