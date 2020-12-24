# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-ctp/rqalpha_mod_ctp/ctp_data_source.py
# Compiled at: 2017-05-26 21:57:31
from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.model.snapshot import SnapshotObject
from rqalpha.utils.logger import system_log
from datetime import date

class CtpDataSource(BaseDataSource):

    def __init__(self, env, md_gateway, trade_gateway):
        path = env.config.base.data_bundle_path
        super(CtpDataSource, self).__init__(path)
        self._md_gateway = md_gateway
        self._md_gateway = trade_gateway

    def current_snapshot(self, instrument, frequency, dt):
        if frequency != 'tick':
            raise NotImplementedError
        order_book_id = instrument.order_book_id
        tick_snapshot = self._md_gateway.snapshot.get(order_book_id)
        if tick_snapshot is None:
            system_log.error('Cannot find such tick whose order_book_id is {} ', order_book_id)
        return SnapshotObject(instrument, tick_snapshot, dt)

    def available_data_range(self, frequency):
        if frequency != 'tick':
            raise NotImplementedError
        s = date.today()
        e = date.fromtimestamp(2147483647)
        return (s, e)

    def get_future_info(self, instrument, hedge_type):
        order_book_id = instrument.order_book_id
        try:
            underlying_symbol = self._trading_dates.get_ins_dict(order_book_id).underlying_symbol
            hedge_flag = hedge_type.value
            return self._trading_dates.get_future_info(underlying_symbol).get(hedge_flag)
        except AttributeError:
            return

        return