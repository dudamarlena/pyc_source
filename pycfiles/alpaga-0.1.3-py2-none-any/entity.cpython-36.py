# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alpaca_trade_api_fixed/entity.py
# Compiled at: 2020-02-14 14:55:34
# Size of source mod 2**32: 3600 bytes
import pandas as pd, pprint, re
ISO8601YMD = re.compile('\\d{4}-\\d{2}-\\d{2}T')
NY = 'America/New_York'

class Entity(object):
    """Entity"""

    def __init__(self, raw):
        self._raw = raw

    def __getattr__(self, key):
        if key in self._raw:
            val = self._raw[key]
            if isinstance(val, str):
                if key.endswith('_at') or key.endswith('_timestamp') or key.endswith('_time'):
                    if ISO8601YMD.match(val):
                        return pd.Timestamp(val)
            return val
        else:
            return super().__getattribute__(key)

    def __repr__(self):
        return '{name}({raw})'.format(name=(self.__class__.__name__),
          raw=pprint.pformat((self._raw), indent=4))


class Account(Entity):
    pass


class Asset(Entity):
    pass


class Order(Entity):
    pass


class Position(Entity):
    pass


class Bar(Entity):

    def __getattr__(self, key):
        if key == 't':
            val = self._raw[key[0]]
            return pd.Timestamp(val, unit='s', tz=NY)
        else:
            return super().__getattr__(key)


class Bars(list):

    def __init__(self, raw):
        super().__init__([Bar(o) for o in raw])
        self._raw = raw

    @property
    def df(self):
        if not hasattr(self, '_df'):
            df = pd.DataFrame((self._raw),
              columns=('t', 'o', 'h', 'l', 'c', 'v'))
            alias = {'t':'time', 
             'o':'open', 
             'h':'high', 
             'l':'low', 
             'c':'close', 
             'v':'volume'}
            df.columns = [alias[c] for c in df.columns]
            df.set_index('time', inplace=True)
            if not df.empty:
                df.index = pd.to_datetime(((df.index * 1000000000.0).astype('int64')),
                  utc=True).tz_convert(NY)
            else:
                df.index = pd.to_datetime((df.index),
                  utc=True)
            self._df = df
        return self._df


class BarSet(dict):

    def __init__(self, raw):
        for symbol in raw:
            self[symbol] = Bars(raw[symbol])

        self._raw = raw

    @property
    def df(self):
        """## Experimental """
        if not hasattr(self, '_df'):
            dfs = []
            for symbol, bars in self.items():
                df = bars.df.copy()
                df.columns = pd.MultiIndex.from_product([
                 [
                  symbol], df.columns])
                dfs.append(df)

            if len(dfs) == 0:
                self._df = pd.DataFrame()
            else:
                self._df = pd.concat(dfs, axis=1)
        return self._df


class Clock(Entity):

    def __getattr__(self, key):
        if key in self._raw:
            val = self._raw[key]
            if key in ('timestamp', 'next_open', 'next_close'):
                return pd.Timestamp(val)
            return val
        else:
            return super().__getattr__(key)


class Calendar(Entity):

    def __getattr__(self, key):
        if key in self._raw:
            val = self._raw[key]
            if key in ('date', ):
                return pd.Timestamp(val)
            if key in ('open', 'close'):
                return pd.Timestamp(val).time()
            return val
        else:
            return super().__getattr__(key)