# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /openexchangerate.py
# Compiled at: 2018-04-11 09:56:50
# Size of source mod 2**32: 5594 bytes
"""OpenExchangeRates API Client for Python 3.6+.

Get your API Key for Free at https://openexchangerates.org/account/app-ids."""
import decimal
from collections import namedtuple
from datetime import datetime
from json import dumps, loads
from types import MappingProxyType as frozendict
from urllib.parse import urlencode
from urllib.request import urlopen
__version__ = '1.5.5'
__all__ = ('OpenExchangeRatesClient', )

class _RoundedFloat(float):
    __doc__ = 'Float that rounds to 2 when repr it, Private.'
    __slots__ = ()

    def __str__(self):
        value = str(round(self, 2))
        if value == '0.0':
            value = str(round(self, 6))
        return value


class OpenExchangeRates(object):
    __doc__ = 'Client for openexchangerate.org.'
    __slots__ = ('api_key', 'timeout', 'use_float', 'round_float', 'base', 'local_base',
                 'tipe', 'html_table_header')
    BASE_URL = 'https://openexchangerates.org/api'
    ENDPOINT_LATEST = BASE_URL + '/latest.json'
    ENDPOINT_CURRENCIES = BASE_URL + '/currencies.json'
    ENDPOINT_HISTORICAL = BASE_URL + '/historical/%s.json'

    def __init__(self, api_key: str, timeout: int=60, use_float: bool=True, round_float: bool=True, base: str='USD', local_base: str=None):
        self.api_key = str(api_key).strip()
        self.timeout = int(timeout)
        self.local_base = local_base
        self.base = str(base).upper()
        self.use_float = use_float
        self.round_float = round_float
        self.html_table_header = True
        self.tipe = _RoundedFloat
        if self.use_float:
            if not self.round_float:
                self.tipe = float
        if not self.use_float:
            self.tipe = decimal.Decimal

    def _parsed_response(self, response):
        data = loads(response, parse_int=(self.tipe), parse_float=(self.tipe))['rates']
        if self.local_base:
            data = self._local_conversion(data, self.local_base)
        return namedtuple('OpenExchangeRates', 'dict frozendict html namedtuple')(data, frozendict(data), self.html(data), (namedtuple('OpenExchangeRates', data.keys()))(*data.values()))

    def _local_conversion(self, data, local_base):
        """Change base using local conversion,offline,useful for free plan."""
        new_rates = {}
        for curr, value in data.items():
            new_rates[curr] = round(value / data[local_base], 8)

        return new_rates

    def latest(self):
        """Fetches latest exchange rate data from openexchangerates."""
        url = f"{self.ENDPOINT_LATEST}?{urlencode({'app_id':self.api_key,  'base':self.base})}"
        response = urlopen(url, timeout=(self.timeout)).read()
        return self._parsed_response(response)

    def currencies(self):
        """Fetches current currency data from openexchangerates."""
        url = f"{self.ENDPOINT_CURRENCIES}?{urlencode({'app_id':self.api_key,  'base':self.base})}"
        data = loads(urlopen(url, timeout=(self.timeout)).read())
        return namedtuple('OpenExchangeRates', 'dict frozendict namedtuple')(data, frozendict(data), (namedtuple('OpenExchangeRates', data.keys()))(*data.values()))

    def historical(self, since_date: datetime):
        """Fetches historical exchange rate data from openexchangerates."""
        if isinstance(since_date, datetime):
            since_date = since_date.strftime('%Y-%m-%d')
        url = f"{self.ENDPOINT_HISTORICAL % since_date}?{urlencode({'app_id':self.api_key,  'base':self.base})}"
        response = urlopen(url, timeout=(self.timeout)).read()
        return self._parsed_response(response)

    def html(self, prices_data_dict: dict):
        names_get = self.currencies().frozendict.get
        prices = tuple(enumerate(prices_data_dict.items()))
        row = '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>'
        h = '<thead><th>#</th><th>Code</th><th>Price</th><th>Name</th></thead>'
        rows = [row.format(index, mony[0], mony[1], names_get(mony[0], '???')) for index, mony in prices if mony[0] not in ('EUR',
                                                                                                                            'USD')]
        prio = [row.format(index, mony[0], mony[1], names_get(mony[0], '???')) for index, mony in prices if mony[0] in ('EUR',
                                                                                                                        'USD')]
        return f"<table>{h if self.html_table_header else ''}<tbody>{' '.join(prio + rows)}</tbody></table>"

    def __enter__(self):
        return self.latest()

    def __exit__(self, exception_type, exception_values, tracebacks, *args):
        pass

    def __iter__(self):
        return iter(self.latest().dict.items())

    def __repr__(self):
        return f"{self.__class__.__name__}(api_key:str={self.api_key}, timeout:int={self.timeout}, use_float:bool={self.use_float}, round_float:bool={self.round_float}, base:str={self.base}, local_base:str={self.local_base}, tipe:type={self.tipe})"

    def __str__(self):
        if self.use_float:
            return dumps((self.latest().dict), sort_keys=True, indent=4).strip()