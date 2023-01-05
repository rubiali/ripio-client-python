import ripio
from ripio.trade.client import Client

ripio.api_key = "U2FsdGVkX1+TMw7DadnWzc5ScM07gbCarakqTfajvqcDoaVdP7uupPeVXY8Pgfs9"  # noqa:E501
new_trade = Client()
new_trade.get_orders(pair="BTC_BRL")
new_trade.get_tickers()
