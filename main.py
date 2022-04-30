import alpaca_trade_api as tradeapi

# Keys needed to access account. Go to alpaca.markets and see Paper Account for your info.
API_KEY = "PKTLRQQ7MTID0G0OA3GT"
API_SECRET = "1XPW4Bw0jNTYvEPdfdis1R1qaTQwsUfOevcVZ0FQ"
API_BASE_URL = 'https://paper-api.alpaca.markets'


# Trading bot. It places orders based on user directions. It should be run and calibrated daily.
# The trading bot is designed for long term strategies. It lowers trade commission and tax costs.
class RealTradeBot(object):
    def __init__(self):
        self.alpaca = tradeapi.REST(API_KEY, API_SECRET, API_BASE_URL)
        self.current_order = None

    def submit_order(self, symbol, qty, side, type, time_in_force, limit_price):

        if self.current_order is not None:
            self.tradeapi.cancel_order(self.current_order.id)

        self.current_order = self.alpaca.submit_order(symbol, qty, side, type, time_in_force, limit_price)
        account = self.alpaca.get_account()

        # Check if our account is restricted from trading.
        if account.trading_blocked:
            print('Account is currently restricted from trading.')

        # Check how much money we can use to open new positions.
        print(f'{side} order submitted for {qty} of {symbol} at {limit_price}')


# This class gives gives an update of the account buying power and a description of the portfolio after buy/sell orders
class AccountUpdate(object):
    def __init__(self):
        self.alpaca = tradeapi.REST(API_KEY, API_SECRET, API_BASE_URL)

    def give_update(self):
        portfolio = self.alpaca.list_positions()
        account = self.alpaca.get_account()

        # Check how much money we can use to open new positions.
        print('${} is your current available as buying power.'.format(account.buying_power))
        print(f'{portfolio} is a list of our positions')


# Cancel all orders so the new orders do not bug the program
class CancelOrders(object):
    def __init__(self):
        self.alpaca = tradeapi.REST(API_KEY, API_SECRET, API_BASE_URL)

    def cancel_orders(self):
        # Cancel open orders so they do not bug the program
        self.alpaca.cancel_all_orders()


# Initialize the trade bot. Add more objects for more stocks.
# Set buy price to "None" if it is a market order
if __name__ == '__main__':
    c = CancelOrders()
    c.cancel_orders()

    goog = RealTradeBot()
    goog.submit_order('GOOG', 1, 'buy', 'limit', 'day', 2900)

    tsla = RealTradeBot()
    tsla.submit_order('TSLA', 5, 'buy', 'limit', 'day', 960)

    coin = RealTradeBot()
    coin.submit_order('COIN', 10, 'buy', 'limit', 'day', 245)

    ivv = RealTradeBot()
    ivv.submit_order('IVV', 10, 'buy', 'market', 'day', None)

    pfe = RealTradeBot()
    pfe.submit_order('PFE', 100, 'buy', 'limit', 'day', 55)

    gme = RealTradeBot()
    gme.submit_order('GME', 200, 'sell', 'limit', 'day', 144)

    # Gives an update on the account after all buy/sell orders have been placed
    update = AccountUpdate()
    update.give_update()
