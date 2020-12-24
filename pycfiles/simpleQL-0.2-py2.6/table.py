# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleql/table.py
# Compiled at: 2011-04-10 18:28:53
from simpleql.filter import get_condition
from simpleql.ordereddict import odict

class LazyDict(odict):

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError


class Table(LazyDict):

    def __init__(self, conn, table, verbose=False):
        odict.__init__(self)
        self.conn = conn
        self.table = table
        self.verbose = verbose
        cur = conn.cursor()
        cur.execute('SELECT * FROM %s LIMIT 1' % self.table)
        cols = [ desc[0] for desc in cur.description ]
        for col in cols:
            self[col] = Col()
            self[col]._simpleql_id = col

    def __iter__(self):
        condition = get_condition(self)
        query = 'SELECT %s FROM %s%s;' % ((', ').join(self._keys), self.table, condition)
        if self.verbose:
            print query
        cur = self.conn.cursor()
        cur.execute(query)
        for values in cur:
            out = LazyDict()
            for (k, v) in zip(self._keys, values):
                out[k] = v

            yield out


class Col(object):
    pass