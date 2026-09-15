from events import MarketEvent, OrderEvent, FillEvent

class ExecutionHandler:
    def __init__(self, commission_rate: float = 0.001):
        self.commission_rate = commission_rate

    def execute_order(self, order_event: OrderEvent, market_event: MarketEvent) -> FillEvent:
        fill_price = market_event.open
        commission = self.commission_rate
        
        fill_event = FillEvent(
            date=market_event.date,
            symbol=order_event.symbol,
            quantity=order_event.quantity,
            direction=order_event.direction,
            fill_price=fill_price,
            commission=commission
        )
        return fill_event