import numpy as np 
import yfinance as yf
import pandas as pd
from strategies import strategy_calc, momentum_strat, mean_reversion_strat
from data import df
from performance import summary

def main():
    momentum_strat(df)
    perf_momentum = summary(df["CumReturn_Momentum"], df["Return_Momentum"], benchmark_returns = df["Return"], label = "Momentum")
    
    df["BH"] = 1
    df["Return_BH"], df["CumReturn_BH"] = strategy_calc(df["BH"], df["Return"])
    perf_BH = summary(df["CumReturn_BH"], df["Return_BH"], benchmark_returns = df["Return"], label = "Buy & Hold")
    
    mean_reversion_strat(df, n=30)
    perf_mean_reversion = summary(df["CumReturn_MeanReversion"], df["Return_MeanReversion"], benchmark_returns = df["Return"], label = "Mean Reversion")
    

    perf = pd.DataFrame([perf_BH, perf_momentum, perf_mean_reversion])
    print(perf)

    print(df["Return_MeanReversion"].sort_values().head(10), df["Return_MeanReversion"].sort_values().tail(10))
    print("skewness = ", df["Return_MeanReversion"].skew())

if __name__ == "__main__":
    main()

