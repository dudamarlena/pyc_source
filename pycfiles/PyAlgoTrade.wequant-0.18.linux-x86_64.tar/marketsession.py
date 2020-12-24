# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/marketsession.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import pytz

class MarketSession(object):
    """Base class for market sessions.

    .. note::
        This is a base class and should not be used directly.
    """

    @classmethod
    def getTimezone(cls):
        """Returns the pytz timezone for the market session."""
        return cls.timezone


class NASDAQ(MarketSession):
    """NASDAQ market session."""
    timezone = pytz.timezone('US/Eastern')


class NYSE(MarketSession):
    """New York Stock Exchange market session."""
    timezone = pytz.timezone('US/Eastern')


class USEquities(MarketSession):
    """US Equities market session."""
    timezone = pytz.timezone('US/Eastern')


class MERVAL(MarketSession):
    """Buenos Aires (Argentina) market session."""
    timezone = pytz.timezone('America/Argentina/Buenos_Aires')


class BOVESPA(MarketSession):
    """BOVESPA (Brazil) market session."""
    timezone = pytz.timezone('America/Sao_Paulo')


class FTSE(MarketSession):
    """ London Stock Exchange market session."""
    timezone = pytz.timezone('Europe/London')


class TSE(MarketSession):
    """Tokyo Stock Exchange market session."""
    timezone = pytz.timezone('Asia/Tokyo')