# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/controllers/stocks_out_today.py
# Compiled at: 2008-07-28 05:37:25
import logging
from datetime import datetime, timedelta
from divimon.lib.base import *
from transaction import TransactionController
from stocks_out import StocksOutController
log = logging.getLogger(__name__)

class StocksOutTodayController(StocksOutController):

    def _list_query(self):
        self.query = model.Session.query(self.table).order_by(self.table.id.desc())
        now = datetime.now()
        today = datetime(now.year, now.month, now.day, 0, 0)
        tomorrow = today + timedelta(1)
        self.query = self.query.filter(self.table.c.created < tomorrow).filter(self.table.c.created >= today)