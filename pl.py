from collections import deque, defaultdict

class Position:
    def __init__(self, name: str):
        self.name = name
        self.size = 0
        self.realized_pnl = 0.0

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

    def sell(self, quantity, price):
        realized_pnl = 0.0
        sell_qty = quantity

        while sell_qty > 0 and self.buys:
            buy_qty, buy_price = self.buys[0]
            match_qty = min(sell_qty, buy_qty)
            
            # Calculate realized P&L for this matched quantity
            realized_pnl += match_qty * (price - buy_price)
            
            # Update remaining quantities
            sell_qty -= match_qty
            if match_qty == buy_qty:
                self.buys.popleft()  # Remove fully used buy
            else:
                self.buys[0] = (buy_qty - match_qty, buy_price)  # Update remaining buy
            
        self.size -= quantity
        self.realized_pnl += realized_pnl
    

positions = defaultdict(Position)

def calc_pnl(trade: dict):
    name = trade["name"]
    position = positions[name]
    if  trade_stock not in positions:
        positions[name] = Position
    
    position = positions[trade_stock]
    position.trade(trade)
    
    return position.realized_pnl



trades = [
    {"stock": "AAPL", "side": "Buy", "quantity": 100, "price": 220.90},
    {"stock": "AAPL", "side": "Buy", "quantity": 200, "price": 221.05},
    {"stock": "AAPL", "side": "Sell", "quantity": 50, "price": 221.10},
    {"stock": "AAPL", "side": "Sell", "quantity": 100, "price": 221.00},
    {"stock": "AAPL", "side": "Buy", "quantity": 100, "price": 203.50},
]

for trade in trades:
    trade_stock = trade["stock"]
    realized_pnl = calc_pnl(trade)
    print(realized_pnl)  

