from enum import IntEnum

class Direction(IntEnum):
    SHORT = -1
    FLAT = 0
    LONG = 1

class Event:
    def __init__(self, event_type: str, date):
        self.event_type = event_type
        self.date = date

class MarketEvent(Event):
    def __init__(self, date, open_, high, low, close, volume):
        super().__init__("MARKET", date)

        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

class SignalEvent(Event):
    def __init__(self, date, actif: str, direction: Direction):
        super().__init__("SIGNAL", date)
        self.actif = actif
        self.direction = direction 

class OrderEvent(Event):
    def __init__(
        self,
        date,
        symbol: str,
        order_type: str,
        quantity: int,
        direction: Direction
    ):
        super().__init__("ORDER", date)

        self.symbol = symbol
        self.order_type = order_type      # "MARKET", "LIMIT", ...
        self.quantity = quantity
        self.direction = direction        

class FillEvent(Event):
    def __init__(
        self,
        date,
        symbol: str,
        quantity: int,
        direction: Direction,
        fill_price: float,
        commission: float = 0.0
    ):
        super().__init__("FILL", date)

        self.symbol = symbol
        self.quantity = quantity
        self.direction = direction
        self.fill_price = fill_price
        self.commission = commission