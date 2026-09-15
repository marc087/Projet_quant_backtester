from data import load_ohlcv
from sizer import FullInvestmentSizer
from data_handler import DataHandler
from strategy_engine import MomentumStrategy
from portfolio import Portfolio
from execution_handler import ExecutionHandler
from performance import cagr
import pandas as pd

def intermediate_test():
    df = load_ohlcv("AAPL", "2020-01-01", "2024-01-01") 
    data_handler = DataHandler(df)
            
    strategy = MomentumStrategy(data_handler, symbol="AAPL", n=60)
    
    for i, bar in enumerate(data_handler):
        if i >= 90:  # premier moment où assez d'historique est disponible
            signal_event = strategy.calculate_signal(bar)
            print(signal_event.date, signal_event.actif, signal_event.direction.name)
        if i > 95:
            break

def run_backtest():
    df = load_ohlcv("AAPL", "2020-01-01", "2024-01-01")
    data_handler = DataHandler(df)
    strategy = MomentumStrategy(data_handler, symbol="AAPL", n=60)
    sizer = FullInvestmentSizer()
    portfolio = Portfolio(initial_cash=10_000, sizer=sizer, symbol="AAPL")
    execution_handler = ExecutionHandler(commission_rate=0.001)

    pending_order = None  # l'ordre en attente d'exécution, décidé au tour précédent

    n_trades = 0

    for market_event in data_handler:
        # 1) on exécute l'ordre en attente s'il y en a un
        if pending_order is not None:
            fill_event = execution_handler.execute_order(pending_order, market_event)
            portfolio.update_fill_event(fill_event)
            pending_order = None  # remis à zéro une fois exécuté
            n_trades += 1
        # 2) on enregistre la valeur du portefeuille du jour
        portfolio.update_history(market_event, market_event.close)

        # 3) on calcule le signal du jour
        signal_event = strategy.calculate_signal(market_event)

        # 4) on demande s'il faut un nouvel ordre
        order_event = portfolio.get_order_event(signal_event, market_event.close)

        # 5) on stocke l'odre pour exécution au prochain tour
        if order_event is not None:
            pending_order = order_event

    cagr_val = cagr(pd.Series([x[1] / portfolio.initial_cash for x in portfolio.history]))
    print("CAGR :", cagr_val, "\nNombre de trades :", n_trades)
    return portfolio