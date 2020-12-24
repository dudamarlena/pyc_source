# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\factor_out_cache.py
# Compiled at: 2018-04-10 01:54:00
# Size of source mod 2**32: 2210 bytes
import sqlite3, pickle, threading
tsp_reference = threading.local()

class FactorOutCache(object):

    def __init__(self):
        self.extra_rows = 0
        self.cache_value = {}

    def addCache(self, date, value):
        self.cache_value[date] = value

    def getCache(self, date):
        try:
            return self.cache_value[date]
        except KeyError:
            return

    def clearCache(self):
        self.cache_value.clear()


class FactorOutMemCache(object):

    def __init__(self):
        self.tsps = {}

    def __getitem__(self, factor):
        tsp = tsp_reference.tsp
        if tsp not in self.tsps.keys():
            self.tsps[tsp] = {}
        if factor not in self.tsps[tsp].keys():
            self.tsps[tsp][factor] = FactorOutCache()
        return self.tsps[tsp][factor]

    def clear(self):
        self.tsps.clear()

    def remove(self, tsp):
        if tsp in self.tsps.keys():
            del self.tsps[tsp]


class FactorOutSqliteCache(object):

    def __init__(self):
        self.conn = sqlite3.connect('factor_out_cache.db')
        c = self.conn.cursor()
        c.execute('drop table if exists out_cache')
        c.execute('create table out_cache\n            (id int not null,\n            f_date text not null,\n            f_out text not null);')
        c.close()
        self.conn.commit()

    def addCache(self, factor_id, factor_date, factor_out):
        c = self.conn.cursor()
        for t in [(factor_id, factor_date, pickle.dumps(factor_out).hex())]:
            c.execute('insert into out_cache(id,f_date,f_out) values(?,?,?)', t)

        c.close()
        self.conn.commit()

    def loadCache(self, factor_id, factor_date):
        c = self.conn.cursor()
        c.execute('select f_out from out_cache where id=? and f_date=?', (factor_id, factor_date))
        rows = c.fetchall()
        if len(rows) == 0:
            return
        else:
            return pickle.loads(bytes.fromhex(rows[0][0]))


factorOutCache = FactorOutMemCache()