from lumibot.brokers import Alpaca #broker
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy #actual trading bot
from lumibot.traders import Trader
from datetime import datetime
from dotenv import load_dotenv
import os
from alpaca_trade_api import REST 
from timedelta import Timedelta # easier to calculate difference between dates
from finbert_utils import estimate_sentiment
import sys
from helpers import convert_date

input_symbol = sys.argv[1]
input_startdate = convert_date(sys.argv[2])
input_enddate = convert_date(sys.argv[3])

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
    def initialize(self, symbol:str, cash_at_risk: float=0.5):
        self.symbol = symbol
        self.sleeptime = "24H" # how frequently we're going to trade
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id= API_KEY, secret_key= API_SECRET)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0) # rounding down
        return cash, last_price, quantity

    def get_dates(self):
        today = self.get_datetime() # current date based on the backtest
        three_days_prior = today - Timedelta(days=3)
        # format date as string for api
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
        # formatting news
        news= [event.__dict__["_raw"]["headline"] for event in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment

    # runs every time we get new data
    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        if cash > last_price: # ensuring not buying when we don't have cash
            if sentiment == 'positive' and probability > 0.999:
                # close existing short positions
                if self.last_trade == 'sell':
                    self.sell_all()
                #place buy order
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy", 
                    type="bracket", # setting floor and ceiling boundaries to sell
                    take_profit_price = last_price * 1.20, 
                    stop_loss_price= last_price * 0.95,
                )
                self.submit_order(order)
                self.last_trade = "buy"

            elif sentiment == 'negative' and probability > 0.999:
                # close existing long positions
                if self.last_trade == 'buy':
                    self.sell_all()
                # place sell order
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell", 
                    type="bracket", # setting floor and ceiling boundaries to sell
                    take_profit_price = last_price * 0.8, # take it
                    stop_loss_price= last_price * 1.05, # prevent future loss
                )
                self.submit_order(order)
                self.last_trade = "sell"

# start_date = datetime(2020, 1, 1)
# end_date = datetime(2023, 12, 31)

broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker, parameters={"symbol": input_symbol, "cash_at_risk" : 0.5})

#evalutate how well our bot performs
strategy.backtest(
    YahooDataBacktesting,
    input_startdate,
    input_enddate,
    parameters={"symbol": input_symbol, "cash_at_risk" : 0.5}
) 