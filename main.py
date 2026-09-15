from v1 import v1
from engine import run_backtest


def main():
    portfolio = run_backtest()
    print(portfolio.history[-5:])

if __name__ == "__main__":
    main()

