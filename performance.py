import numpy as np
import pandas as pd 

TRADING_DAYS_PER_YEAR = 252


def cagr(cum_returns: pd.Series) -> float:
    cum_returns = cum_returns.dropna()

    if cum_returns.empty:
        raise ValueError("La série est vide.")
    
    # cum_returns[-1]/cum_returns[0] = valeur_finale / valeur_initiale
    n_year = len(cum_returns)/TRADING_DAYS_PER_YEAR
    return (cum_returns.iloc[-1] / cum_returns.iloc[0])**(1/n_year) - 1

def volatility(returns: pd.Series) -> float:
    daily_sigma = returns.std(ddof=1)  # écart type empirique
    return daily_sigma * np.sqrt(TRADING_DAYS_PER_YEAR)

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    annual_sigma = volatility(returns)
    annual_R = returns.mean() * TRADING_DAYS_PER_YEAR
    return (annual_R - risk_free_rate) / annual_sigma

def sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    # downside_returns = returns[returns < 0] réduit énormément l'échantillon pour mean reversion --- voir tests
    downside_returns = returns.clip(upper=0) # min(rt,0)
    # downside_returns_sigma = downside_returns.std(ddof=1)
    downside_returns_sigma = np.sqrt((downside_returns**2).mean())
    annual_downside_returns_sigma = downside_returns_sigma * np.sqrt(TRADING_DAYS_PER_YEAR)
    annual_R = returns.mean() * TRADING_DAYS_PER_YEAR
    return (annual_R - risk_free_rate)/annual_downside_returns_sigma

def max_drawdown(cum_returns: pd.Series) -> float:
    cum_returns = cum_returns.dropna()

    if cum_returns.empty:
            raise ValueError("La série est vide.")
    
    pic_max = cum_returns.cummax()
    rel_dif = (cum_returns - pic_max) / pic_max
    return np.min(rel_dif)

def alpha_beta(returns: pd.Series, benchmark_returns: pd.Series, risk_free_rate: float = 0.0) -> tuple[float, float]:
    # 1. Aligner et nettoyer les deux séries ensemble
    combined = pd.concat([returns, benchmark_returns], axis=1)
    combined.columns = ["strategy", "benchmark"]
    combined = combined.dropna()

    if combined.empty:
            raise ValueError("La série est vide.")

    # 2. Beta = covariance(stratégie, benchmark) / variance(benchmark)
    beta = combined["strategy"].cov(combined["benchmark"]) / combined["benchmark"].var()

    # 3. Rendements annualisés des deux séries
    annual_R = combined["strategy"].mean() * TRADING_DAYS_PER_YEAR
    annual_benchmark_R = combined["benchmark"].mean() * TRADING_DAYS_PER_YEAR

    # 4. Alpha à partir de beta et des deux rendements annualisés
    alpha = (annual_R - risk_free_rate) - beta * (annual_benchmark_R - risk_free_rate)

    return alpha, beta

def summary(cum_returns: pd.Series, returns: pd.Series, benchmark_returns: pd.Series = None, label: str = "") -> dict:
    performance = {"Label": label}
    
    performance["CAGR"] = cagr(cum_returns)
    performance["Volatility"] = volatility(returns)
    performance["Sharpe"] = sharpe_ratio(returns)
    performance["Sortino"] = sortino_ratio(returns)
    performance["MaxDrawdown"] = max_drawdown(cum_returns)
    
    if benchmark_returns is not None:
        performance["Alpha"], performance["Beta"] = alpha_beta(returns, benchmark_returns, 0.0)

    return performance