# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\bitstamp\common.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 948 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import pyalgotrade.logger
from pyalgotrade import broker
logger = pyalgotrade.logger.getLogger('bitstamp')
btc_symbol = 'BTC'

class BTCTraits(broker.InstrumentTraits):

    def roundQuantity(self, quantity):
        return round(quantity, 8)