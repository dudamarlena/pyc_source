# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-vnpy/rqalpha_mod_vnpy/vnpy_broker.py
# Compiled at: 2017-05-22 05:49:49
from rqalpha.interface import AbstractBroker
from rqalpha.environment import Environment
from rqalpha.model.account import BenchmarkAccount, FutureAccount
from rqalpha.const import ACCOUNT_TYPE

def init_accounts(env):
    accounts = {}
    config = env.config
    start_date = config.base.start_date
    total_cash = 0
    future_starting_cash = config.base.future_starting_cash
    accounts[ACCOUNT_TYPE.FUTURE] = FutureAccount(env, future_starting_cash, start_date)
    if config.base.benchmark is not None:
        accounts[ACCOUNT_TYPE.BENCHMARK] = BenchmarkAccount(env, total_cash, start_date)
    return accounts


class VNPYBroker(AbstractBroker):

    def __init__(self, gateway):
        self._gateway = gateway
        self._open_orders = []

    def after_trading(self):
        pass

    def before_trading(self):
        self._gateway.connect_and_sync_data()
        for account, order in self._open_orders:
            order.active()
            self._env.event_bus.publish_event(Event(EVENT.ORDER_CREATION_PASS, account=account, order=order))

    def get_open_orders(self, order_book_id=None):
        if order_book_id is not None:
            return [ order for order in self._gateway.open_orders if order.order_book_id == order_book_id ]
        else:
            return self._gateway.open_orders
            return

    def submit_order(self, order):
        self._gateway.submit_order(order)

    def cancel_order(self, order):
        self._gateway.cancel_order(order)

    def update(self, calendar_dt, trading_dt, bar_dict):
        pass

    def get_portfolio(self):
        return self._gateway.get_portfolio()

    def get_benchmark_portfolio(self):
        return