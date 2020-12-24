# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-ctp/rqalpha_mod_ctp/ctp_price_board.py
# Compiled at: 2017-05-26 22:17:15
from rqalpha.interface import AbstractPriceBoard
from rqalpha.utils.logger import system_log

class CtpPriceBoard(AbstractPriceBoard):

    def __init__(self, md_gateway, trade_gateway):
        self._md_gateway = md_gateway
        self._trade_gateway = trade_gateway

    def get_last_price(self, order_book_id):
        tick_snapshot = self._md_gateway.snapshot.get(order_book_id)
        if tick_snapshot is None:
            tick_snapshot = self._trade_gateway.snapshot.get(order_book_id)
        if tick_snapshot is None:
            system_log.error('Cannot find such tick whose order_book_id is {} ', order_book_id)
            return
        else:
            return tick_snapshot['last']

    def get_limit_up(self, order_book_id):
        tick_snapshot = self._md_gateway.snapshot.get(order_book_id)
        if tick_snapshot is None:
            system_log.error('Cannot find such tick whose order_book_id is {} ', order_book_id)
            return
        else:
            return tick_snapshot['limit_up']

    def get_limit_down(self, order_book_id):
        tick_snapshot = self._md_gateway.snapshot.get(order_book_id)
        if tick_snapshot is None:
            system_log.error('Cannot find such tick whose order_book_id is {} ', order_book_id)
            return
        else:
            return tick_snapshot['limit_down']