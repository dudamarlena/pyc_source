# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/bitstamp/common.py
# Compiled at: 2016-11-29 01:45:48
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