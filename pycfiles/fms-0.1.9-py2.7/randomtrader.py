# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fms/agents/randomtrader.py
# Compiled at: 2011-06-13 22:36:15
"""
Module defining RandomTrader agent class.
"""
import random, logging
from fms import agents
from fms.utils import BUY, SELL
from fms.utils.exceptions import MissingParameter
logger = logging.getLogger('fms.agents.randomtrader')

class RandomTrader(agents.Agent):
    """
    Simulate an agent taking random but not stupid decisions

    This agent subclass should have three keys in the
    args dict :
    - avgprice : average order price (float)
    - maxfluct : maximum % fluctuation around price (int)
    - maxbuy : maximum quantity to buy (int)
    If any of those parameters is missing, a MissingParameter
    exception is raised.
    >>> from fms.agents import randomtrader
    >>> params = {'agents': [{'money':10000, 'stocks':200}]}
    >>> agent = randomtrader.RandomTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: avgprice
    >>> params = {'agents': [{'money':10000, 'stocks':200, 'args':[100]}]}
    >>> agent = randomtrader.RandomTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: maxfluct
    >>> params = {'agents': [{'money':10000, 'stocks':200, 'args':[100, 20]}]}
    >>> agent = randomtrader.RandomTrader(params)
    Traceback (most recent call last):
        ...
    MissingParameter: maxbuy
    >>> params = {'agents': [{'money':10000, 'stocks':200, 'args':[100, 20, 200]}]}
    >>> agent = randomtrader.RandomTrader(params)
    >>> print agent.state()
    Agent ... - owns $10000.00 and    200 securities
    >>> print agent.avgprice
    100
    >>> print agent.maxfluct
    20
    >>> print agent.maxbuy
    200

    The RandomTrader acts by returning a
    dict with (direction, price, quantity) keys.
    >>> len(agent.act())
    3
    
    If avgprice is 0 then the last transaction price is used.
    - direction is buy or sell
    - price is a %.2f float in 
      [avgprice*(1-maxfluct/100), avgprice*(1+maxfluct/100)]
    - quantity is an int in :
      - if direction==BUY, [1,self.maxbuy]
      - if direction==SELL, [1,self.stocks]
    But quantity is strictly controlled :
    neither shortselling nor buy position without required cash
    are allowed.
    >>> order = agent.act()
    >>> order['price'] >= 80
    True
    >>> order['price'] <= 120
    True

    """

    def __init__(self, params, offset=0):
        agents.Agent.__init__(self, params, offset)
        try:
            self.avgprice = self.args[0]
        except (AttributeError, IndexError):
            raise MissingParameter, 'avgprice'

        try:
            self.maxfluct = self.args[1]
        except IndexError:
            raise MissingParameter, 'maxfluct'

        try:
            self.maxbuy = self.args[2]
        except IndexError:
            raise MissingParameter, 'maxbuy'

        del self.args

    def act(self, world=None, market=None):
        """
        Return random order as a dict with keys in (direction, price, quantity).
        """
        if self.stocks > 0:
            direction = random.choice((BUY, SELL))
        else:
            direction = BUY
        if self.avgprice == 0:
            try:
                self.avgprice = market.lastprice
            except AttributeError:
                self.avgprice = 100
                logger.warning('No market, no avgprice, avgprice set to 100')

        price = random.randint(self.avgprice * (100 - self.maxfluct), self.avgprice * (100 + self.maxfluct)) / 100.0
        if direction:
            maxq = self.stocks
        else:
            maxq = min(self.maxbuy, int(self.money / price))
        try:
            quantity = random.randint(1, maxq)
        except ValueError:
            quantity = 1

        return {'direction': direction, 'price': price, 'quantity': quantity}


def _test():
    """
    Run tests in docstrings
    """
    import doctest
    doctest.testmod(optionflags=+doctest.ELLIPSIS)


if __name__ == '__main__':
    _test()