from collections import deque, defaultdict
from decimal import Decimal

class Position:
    def __init__(self):
        self.size = 0
        self.realized_pnl = 0.0

        # FIFO queue for buys
        self.buys = deque()  

    def trade(self, trade):
        # mutex lock

        
        if trade["side"] == "Buy":
            self.buy(trade["quantity"], trade["price"])
        else:
            self.sell(trade["quantity"], trade["price"])

    def buy(self, quantity, price):
        self.buys.append((quantity, price))
        self.size += quantity
        print(f"Buy {quantity}, {price}, {self.buys}, {self.realized_pnl}")

    def sell(self, quantity, price):
        realized_pnl = 0.0
        sell_qty = quantity

        while sell_qty > 0 and self.buys:
            buy_qty, buy_price = self.buys[0]
            match_qty = min(sell_qty, buy_qty)
            
            # Calculate realized P&L for the matched quantity
            realized_pnl += match_qty * (price - buy_price)
            print(f"match_qty={match_qty}, sell_price={price}, buy_price={buy_price}, {price - buy_price}, realized_pnl={realized_pnl}")
            
            # Update remaining quantities
            sell_qty -= match_qty
            if match_qty == buy_qty:
                # Remove the completely realized buy order
                self.buys.popleft()  
            else:
                self.buys[0] = (buy_qty - match_qty, buy_price)  # Update remaining buy
            
        self.size -= quantity
        self.realized_pnl = realized_pnl
        print(f"Sell {quantity}, {price}, {self.buys}, {self.realized_pnl}")
    

positions = defaultdict(Position)

def calc_pnl(trade: dict):
    stock = trade["stock"]
    position = positions[stock]
    if  stock not in positions:
        positions[stock] = Position()
    
    position = positions[stock]
    position.trade(trade)
    
    return position.realized_pnl



trades = [
    {"stock": "AAPL", "side": "Buy", "quantity": 100, "price": 220.90},
    {"stock": "AAPL", "side": "Buy", "quantity": 200, "price": 221.05},
    {"stock": "AAPL", "side": "Sell", "quantity": 50, "price": 221.10},
    {"stock": "AAPL", "side": "Sell", "quantity": 100, "price": 221.00},
    {"stock": "IBM", "side": "Buy", "quantity": 100, "price": 203.50},
]

for trade in trades:
    realized_pnl = calc_pnl(trade)

