# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/controllers/markup.py
# Compiled at: 2008-07-28 05:37:25
import logging
from divimon.lib.base import *
from transaction import TransactionController
from stocks_out import StocksOutController
log = logging.getLogger(__name__)

class MarkupController(ListController):
    table = model.Transaction

    def daily(self):
        return render('/budget/daily_markup.mako')

    def weekly(self):
        return render('/budget/weekly_markup.mako')

    def index(self, id):
        return id