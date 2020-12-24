# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\marketsession.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 2248 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import pytz

class MarketSession(object):
    __doc__ = 'Base class for market sessions.\n\n    .. note::\n        This is a base class and should not be used directly.\n    '

    @classmethod
    def getTimezone(cls):
        """Returns the pytz timezone for the market session."""
        return cls.timezone


class NASDAQ(MarketSession):
    __doc__ = 'NASDAQ market session.'
    timezone = pytz.timezone('US/Eastern')


class NYSE(MarketSession):
    __doc__ = 'New York Stock Exchange market session.'
    timezone = pytz.timezone('US/Eastern')


class USEquities(MarketSession):
    __doc__ = 'US Equities market session.'
    timezone = pytz.timezone('US/Eastern')


class MERVAL(MarketSession):
    __doc__ = 'Buenos Aires (Argentina) market session.'
    timezone = pytz.timezone('America/Argentina/Buenos_Aires')


class BOVESPA(MarketSession):
    __doc__ = 'BOVESPA (Brazil) market session.'
    timezone = pytz.timezone('America/Sao_Paulo')


class FTSE(MarketSession):
    __doc__ = ' London Stock Exchange market session.'
    timezone = pytz.timezone('Europe/London')


class TSE(MarketSession):
    __doc__ = 'Tokyo Stock Exchange market session.'
    timezone = pytz.timezone('Asia/Tokyo')