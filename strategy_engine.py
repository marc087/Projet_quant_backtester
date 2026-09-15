from events import Direction, SignalEvent
from strategies import perf_N, generate_momentum_signal

class Strategy:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def calculate_signal(self, market_event) -> SignalEvent:
        raise NotImplementedError("Les classes filles doivent implémenter cette méthode")


class MomentumStrategy(Strategy):
    def __init__(self, data_handler, symbol: str, n: int = 60):
        super().__init__(data_handler) 
        self.symbol = symbol
        self.n = n

    def calculate_signal(self, market_event) -> SignalEvent:
        history = self.data_handler.get_latest_bars(self.n + 1)
        perf = perf_N(history["Close"], self.n)
        signal = generate_momentum_signal(perf)
        
        if signal.size > 0:
            direction = Direction(signal[-1])
        else:
            direction = Direction.FLAT

        signal_event = SignalEvent(date=market_event.date, actif=self.symbol ,direction=direction)

        return signal_event
