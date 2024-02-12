from lumibot.brokers import Alpaca #broker
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy #actual trading bot
from lumibot.traders import Trader
from datetime import datetime
from dotenv import load_dotenv
import os

#loading credentials
if "API_KEY" not in os.environ: # local retrieval of environment variables
    load_dotenv()

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]

BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "API_KEY" : API_KEY,
    "API_SECRET" : API_SECRET,
    "PAPER": True, # paper trading not dropping in real cash
}

# inherits from Strategy class
class MLTrader(Strategy):
    # only runs once
    def initialize(self, symbol:str="SPY", cash_at_risk: float=0.5):
        self.symbol = symbol
        self.sleeptime = "24H" # how frequently we're going to trade
        self.last_trade = None
        self.cash_at_risk = cash_at_risk

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)



    # runs every time we get new data
    def on_trading_iteration(self):
        if self.last_trade == None:
            order = self.create_order(
                self.symbol,
                10,
                "buy", 
                type="market"
            )
            self.submit_order(order)
            self.last_trade = "buy"

start_date = datetime(2023, 12, 15)
end_date = datetime(2023, 12, 31)

broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker, parameters={"symbol": "SPY"})

#evalutate how well our bot performs
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
) 