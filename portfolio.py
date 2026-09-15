from sizer import Sizer
from events import Direction, MarketEvent, SignalEvent, OrderEvent, FillEvent

class Portfolio:
    def __init__(self, initial_cash: float, sizer: Sizer, symbol: str):
        self.cash = initial_cash
        self.initial_cash = initial_cash    # gardé de côté pour le calcul final de CumReturn
        self.position = 0                          # nombre d'actions détenues
        self.current_direction = Direction.FLAT    # état de départ : pas investi
        self.sizer = sizer
        self.symbol = symbol
        self.history = []                           # pour reconstruire CumReturn à la fin, liste de (date, valeur_totale)

    def get_order_event(self, signal_event: SignalEvent, current_price: float) -> OrderEvent | None:
        if signal_event.direction == self.current_direction:
            return None  # pas de changement, rien à faire

        quantity = self.sizer.calculate_quantity(
            direction=signal_event.direction,
            price=current_price,
            current_position=self.position,
            cash=self.cash
        )

        order_event = OrderEvent(
            date=signal_event.date,
            symbol=self.symbol,
            order_type="MARKET",
            quantity=quantity,
            direction=signal_event.direction
        )
        return order_event

    def update_fill_event(self, fill_event: FillEvent):
        if fill_event.direction == Direction.LONG:
            self.cash -= fill_event.quantity * fill_event.fill_price * (1 + fill_event.commission)
            self.position += fill_event.quantity
        elif fill_event.direction == Direction.FLAT:
            self.cash += fill_event.quantity * fill_event.fill_price * (1 - fill_event.commission)
            self.position -= fill_event.quantity

        self.current_direction = fill_event.direction

    def update_history(self, market_event: MarketEvent, current_price: float):
        self.history.append((market_event.date, self.cash + self.position * current_price))
            
