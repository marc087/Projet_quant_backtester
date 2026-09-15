import pandas as pd
from events import MarketEvent

class DataHandler:
    def __init__(self, df: pd.DataFrame):
        self.data = df
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self) -> MarketEvent:
        if self.current_index >= len(self.data):
            raise StopIteration
        
        else:
            bar = self.data.iloc[self.current_index]
            market_event = MarketEvent(bar.name,
                                       bar["Open"],
                                       bar["High"],
                                       bar["Low"],
                                       bar["Close"],
                                       bar["Volume"])

            self.current_index += 1
            return market_event

    def get_latest_bars(self, n: int) -> pd.DataFrame:
        return self.data.iloc[max(0, self.current_index - n - 1) : self.current_index]