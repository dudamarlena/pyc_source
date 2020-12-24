# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-ctp/rqalpha_mod_ctp/ctp_broker.py
# Compiled at: 2017-05-26 22:09:45
from rqalpha.interface import AbstractBroker

class CtpBroker(AbstractBroker):

    def __init__(self, trading_gateway):
        super(CtpBroker, self).__init__()
        self._trading_gateway = trading_gateway
        self._open_orders = []

    def after_trading(self):
        pass

    def before_trading(self):
        self._trading_gateway.connect()
        for account, order in self._trading_gateway.open_orders:
            order.active()
            self._env.event_bus.publish_event(Event(EVENT.ORDER_CREATION_PASS, account=account, order=order))

    def get_open_orders(self, order_book_id=None):
        if order_book_id is not None:
            return [ order for order in self._trading_gateway.open_orders if order.order_book_id == order_book_id ]
        else:
            return self._trading_gateway.open_orders
            return

    def submit_order(self, order):
        self._trading_gateway.submit_order(order)

    def cancel_order(self, order):
        self._trading_gateway.cancel_order(order)

    def update(self, calendar_dt, trading_dt, bar_dict):
        pass

    def get_portfolio(self):
        return self._trading_gateway.get_portfolio()