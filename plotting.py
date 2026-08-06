import matplotlib.pyplot as plt
import pandas as pd

def plot_equity_curves(df: pd.DataFrame, columns: list[str], labels: list[str], log_scale: bool = True) -> None:
    plt.figure()
    for i in range(len(columns)):
        plt.plot(df.index, df[columns[i]], label = labels[i] )
    plt.yscale('log' if log_scale else 'linear')
    plt.legend()
    plt.xlabel('Trading days')
    plt.ylabel("Courbes d'equity de 3 stratégies")
    plt.savefig("equity_plotting.png")