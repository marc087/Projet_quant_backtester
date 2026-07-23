import numpy as np 
import yfinance as yf
import pandas as pd


# On remarque que décaler le signal d'un jour, multiplier par le rendement du marché, cumuler 
# est générique à toutes les stratégies.
# On peut donc écrire une fonction qui prendrait un signal et un rendement
# en entrée et réutilisable pour toutes les futures stratégies.

def strategy_calc(signal: pd.Series, market_return: pd.Series) -> tuple[pd.Series, pd.Series]:
    # On calcule le rendement de la stratégie
    strat_return = signal.shift(1) * market_return # Le signal est décalé d'un jour pour éviter le biais anticipatif.
    # Puis le rendendement cumulé (on multiplie successivement les rendements)
    cum_strat_return = (1 + strat_return).cumprod()
    return strat_return, cum_strat_return

'''MOMENTUM'''

N = 60 # 2 mois, court terme à comparer plus tard avec 252 (jours de bourse en 1 an)

def perf_N(close, N):
    return close.pct_change(periods=N)

def generate_momentum_signal(rendement):
    return np.where(rendement.isna(), 0, (rendement > 0).astype(int))

def momentum_strat(df):
    df["Return"] = df["Close"].pct_change() # rendement journalier
    df["perf_N"] = perf_N(df["Close"], N)
    df["Signal"] = generate_momentum_signal(df["perf_N"])
    df["Return_Momentum"], df["CumReturn_Momentum"] = strategy_calc(df["Signal"], df["Return"])


'''MEAN REVERSION'''

n = 30 # n relativement petit car les écarts excessifs sont des
       # phénomènes plus courts que les tendances de fond

def z_score(close: pd.Series, n: int) -> pd.Series:
    return (close - close.rolling(n).mean()) / close.rolling(n).std()

def generate_mean_reversion_signal(z: pd.Series, threshold: float = -1.645) -> np.ndarray:
    return np.where(z.isna(), 0, z < threshold).astype(int)

def mean_reversion_strat(df: pd.DataFrame, n: int) -> None:
    df["Return"] = df["Close"].pct_change()
    df["Z_score"] = z_score(df["Close"], n)
    df["Signal"] = generate_mean_reversion_signal(df["Z_score"], threshold=-1.645) 
    df["Return_MeanReversion"], df["CumReturn_MeanReversion"] = strategy_calc(df["Signal"], df["Return"])