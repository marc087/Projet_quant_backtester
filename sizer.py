import math
from events import Direction

class Sizer:
    def calculate_quantity(self, direction: Direction, price: float, current_position: int, cash: float) -> int:
        raise NotImplementedError

class FullInvestmentSizer(Sizer):
    def calculate_quantity(self, direction: Direction, price: float, current_position: int, cash: float) -> int:
        if direction == Direction.LONG:
            return math.floor(cash/price)
        
        elif direction == Direction.FLAT:              
            return current_position
                
        else: 
            raise ValueError("Short not coded yet")