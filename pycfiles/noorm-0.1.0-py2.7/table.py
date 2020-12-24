# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noorm/table.py
# Compiled at: 2017-05-07 07:09:55
import sqlite3

class Table(object):

    def __init__(self, parent, tablename):
        self.parent = parent
        self.tablename = tablename

    def __getitem__(self, parameter):
        if isinstance(parameter, (int, long)):
            qry = ('select * from {} where id=?').format(self.tablename)
            self.parent.cursor.execute(qry, (parameter,))
            result = self.parent.cursor.fetchall()
            assert len(result) == 1, 'there should be exactly one row with this id'
            return result[0]
        else:
            if isinstance(parameter, dict):
                assert len(parameter) > 0
                where = (' and ').join(("{}='{}'").format(k, v) for k, v in parameter.items())
                qry = ('select * from {} where {}').format(self.tablename, where)
                self.parent.cursor.execute(qry)
                return self.parent.cursor.fetchall()
            if isinstance(parameter, slice):
                assert parameter.start is not None
                assert parameter.start >= 0
                start = parameter.start
                assert parameter.stop is not None
                assert parameter.stop > parameter.start
                stop = parameter.stop
                assert parameter.step is None or parameter.step > 0
                step = parameter.step or 1
                rng = range(start, stop, step)
                qry = ('select * from {} where id in ({})').format(self.tablename, (', ').join(['?'] * len(rng)))
                self.parent.cursor.execute(qry, rng)
                return self.parent.cursor.fetchall()
            if isinstance(parameter, (str, unicode)):

                def _all():
                    self.parent.cursor.execute(('select * from {}').format(self.tablename))
                    return self.parent.cursor.fetchall()

                def _err():
                    raise TypeError(('{} is not supported: {}').format(type(parameter), parameter))

                it = unicode(parameter)
                actions = {'*': _all, 
                   'all': _all}
                return actions.get(it, _err)()
            raise TypeError(('{} is not supported: {}').format(type(parameter), parameter))
            return

    def insert(self, data):
        if 'id' in data:
            raise Exception("'id' may not be in the dictionary. Did you want to use update(...)")
        keys = []
        values = []
        for k, v in data.items():
            keys.append(k)
            values.append(v)

        qry = ('insert into {} ({}) values ({})').format(self.tablename, (', ').join(keys), (', ').join(['?'] * len(values)))
        for _ in xrange(len(keys) + 2):
            try:
                self.parent.cursor.execute(qry, values)
            except sqlite3.OperationalError as oe:
                if oe.message.startswith(('table {} has no column named ').format(self.tablename)):
                    colname = oe.message.split()[(-1)]
                    alter_qry = ('alter table {} add column {}').format(self.tablename, colname)
                    self.parent.cursor.execute(alter_qry)
                    continue
                elif oe.message.startswith('no such table:'):
                    self.parent.cursor.execute(('create table if not exists {} (id INTEGER PRIMARY KEY)').format(self.tablename))
                    continue
                raise

            break

    def update(self, data):
        assert isinstance(data, dict)
        assert isinstance(data['id'], (int, long))
        upd = {}
        upd.update(data)
        del upd['id']
        keys = []
        values = []
        for k, v in upd.items():
            keys.append(k)
            values.append(v)

        qry = ('update {} set {} where id = ?').format(self.tablename, (', ').join(('{} = ?').format(key) for key in keys))
        self.parent.cursor.execute(qry, values + [data['id']])