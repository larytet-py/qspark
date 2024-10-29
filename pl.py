from collections import deque, defaultdict
from typing import Dict
from decimal import Decimal

class Position:
    def __init__(self, stock: str, tick_size: float):
        self.stock = stock
        self.size = 0
        self.realized_pnl = 0.0
        self.tick_size = tick_size

        # FIFO queue for buys
        self.buys = deque()  

    def trade(self, trade):
        if trade["side"] == "Buy":
            self.buy(trade["quantity"], trade["price"])
        else:
            self.sell(trade["quantity"], trade["price"])

    def buy(self, quantity, price):
        self.buys.append((quantity, price))
        self.size += quantity
        print(f"Buy {self.stock} {quantity}, {price}, {self.buys}, {self.realized_pnl}")

    def sell(self, quantity, price):
        realized_pnl = 0.0
        sell_qty = quantity

        while sell_qty > 0 and self.buys:
            buy_qty, buy_price = self.buys[0]
            match_qty = min(sell_qty, buy_qty)
            
            # Calculate realized P&L for the matched quantity
            pl = self.to_tick(price) - self.to_tick(buy_price)
            realized_pnl += self.from_tick(match_qty * pl)
            print(f"match_qty={match_qty}, sell_price={price}, buy_price={buy_price}, {pl}, realized_pnl={realized_pnl}")
            
            # Update remaining quantities
            sell_qty -= match_qty
            if match_qty == buy_qty:
                # Remove the completely realized buy order
                self.buys.popleft()  
            else:
                self.buys[0] = (buy_qty - match_qty, buy_price)  # Update remaining buy
            
        self.size -= quantity
        self.realized_pnl = realized_pnl
        print(f"Sell {self.stock} {quantity}, {price}, {self.buys}, {self.realized_pnl}")

    def to_tick(self, v: float) -> int:
        return round(v*self.tick_size)

    def from_tick(self, v: int) -> float:
        return v/self.tick_size


positions: Dict[str, Position] = {}

def calc_pnl(trade: dict):
    stock = trade["stock"]
    if  stock not in positions:
        positions[stock] = Position(stock, trade["tick_size"])
    
    position = positions[stock]
    position.trade(trade)
    
    return position.realized_pnl



trades = [
    {"stock": "AAPL", "side": "Buy", "quantity": 100, "price": 220.90, "tick_size": 100},
    {"stock": "AAPL", "side": "Buy", "quantity": 200, "price": 221.05, "tick_size": 100},
    {"stock": "AAPL", "side": "Sell", "quantity": 50, "price": 221.10, "tick_size": 100},
    {"stock": "AAPL", "side": "Sell", "quantity": 100, "price": 221.00, "tick_size": 100},
    {"stock": "IBM", "side": "Buy", "quantity": 100, "price": 203.50, "tick_size": 100},
]

for trade in trades:
    realized_pnl = calc_pnl(trade)

