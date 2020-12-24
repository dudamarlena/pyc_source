# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/twaldear/Sites/sqliteAdmin-root/flask_sqlite_admin/sqliteFunctions.py
# Compiled at: 2016-06-21 18:12:34
import re
from functools import wraps
import types, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def execRule(i):

    def do_assignment(to_func):
        to_func.run = i
        return to_func

    return do_assignment


class rules:
    """ base rules applied to all modifications """

    def __init__(self, colData, postData, tables, method):
        self.colData = colData
        self.postData = postData
        self.method = method
        self.methods = ['GET', 'POST', 'PUT', 'DELETE']
        self.tables = tables
        if self.colData['name'] in self.postData:
            self.value = self.postData[self.colData['name']]
        else:
            self.value = '0'

    @execRule(1)
    def validTable(self):
        """ check if table is in object """
        if 'table' not in self.postData or self.postData['table'] not in self.tables:
            raise ValueError('invalid table `%s`' % self.postData['table'])

    @execRule(2)
    def validAction(self):
        """ check if action is valid """
        if self.method is None:
            raise ValueError('no method in request')
        elif self.method not in self.methods:
            raise ValueError('invalid method `%s`' % self.method)
        return

    @execRule(3)
    def idRequired(self):
        """ check if id parameter passed for edit/delete functions """
        if self.method == 'put' or self.method == 'delete':
            if 'id' not in self.postData:
                raise ValueError('Request must include an id')

    @execRule(4)
    def notNull(self):
        """ check if null value passed for not null columns """
        if self.colData['name'] not in self.postData or self.value == '':
            if self.colData['notNull'] is 1 and self.colData['primaryKey'] is 0:
                raise ValueError('%s field required' % self.colData['name'])

    @execRule(5)
    def integer(self):
        """ check if integer for integer affinity columns """
        if self.colData['dataType'].lower() in ('integer', 'int', 'tinyint', 'smallint',
                                                'mediumint', 'bigint', 'unisgned big int',
                                                'int2', 'int8'):
            try:
                int(self.value)
            except Exception as e:
                raise ValueError('Non integer value `%s` for field %s' % (self.value, self.colData['name']))

    @execRule(6)
    def real(self):
        """ check if float for real affinity columns """
        if self.colData['dataType'].lower() in ('real', 'float', 'double', 'double precision'):
            try:
                float(self.value)
            except Exception as e:
                raise ValueError('Non real/float value `%s` for field %s' % (self.value, self.colData['name']))


class sqliteAdminFunctions:
    """ functions for SQLite3 Admin tool """

    def __init__(self, con, tables=[], extraRules=[]):
        self.db = con
        self.extraRules = extraRules
        self.tables = self.tableList(tables)

    def dict_factory(self, cursor, row):
        """ function to return sqlite results in dict """
        d = {}
        for idx, col in enumerate(cursor.description):
            try:
                str(row[idx]).decode('utf-8').encode('utf-8')
                d[col[0]] = row[idx]
            except:
                d[col[0]] = 'invalid byte'

        return d

    def tableList(self, tables):
        if len(tables) > 0:
            return tables
        else:
            c = self.db.execute('SELECT name FROM sqlite_master WHERE type = "table"')
            return [ row[0] for row in c.fetchall() ]

    def tableContents(self, table, sort, dir, offset):
        """ create list of tables for admin """
        res = {}
        if table in self.tables:
            res['schema'] = self.tableSchemas(table)
            if res['schema'][0]['primaryKey'] == 1:
                res['primaryKey'] = res['schema'][0]['name']
                con = self.db
                con.row_factory = self.dict_factory
                c = self.db.execute('select count(?) as c from %s' % table, [res['primaryKey']])
                res['count'] = c.fetchone()['c']
                if sort == '':
                    sort = res['primaryKey']
                l = self.db.execute('select * from %s order by %s %s limit ?,50' % (table, sort, dir), [int(offset) * 50])
                res['contents'] = l.fetchall()
                return res
            raise ValueError('No primary key for first column in table `%s`' % table)
        else:
            raise ValueError('invalid table `%s`' % table)

    def tableSchemas(self, table):
        """ return table schemas by column """
        cur = self.db.execute('PRAGMA table_info(%s)' % table)
        return [ {'name': row[1], 'dataType': row[2], 'notNull': row[3], 'primaryKey': row[5]} for row in cur.fetchall() ]

    def checkValid(self, q, method):
        """ validate admin input """
        if 'table' not in q:
            raise ValueError('no table value provided')
        elif q['table'] not in self.tables:
            raise ValueError('invalid table `%s`' % q['table'])
        else:
            for col in self.tableSchemas(q['table']):
                r = rules(col, q, self.tables, method)
                if len(self.extraRules) > 0:
                    for i, x in enumerate(self.extraRules):
                        x.run = 7 + i

                        def add_method(self, method, i):
                            setattr(self.__class__, 'extraRule%d' % i, method)

                        add_method(r, x, i)

                funcs = sorted([ getattr(r, field) for field in dir(r) if hasattr(getattr(r, field), 'run') ], key=lambda field: field.run)
                for func in funcs:
                    try:
                        func()
                    except Exception as e:
                        raise

    def editTables(self, q, method):
        """ edit tables """
        qString = ''
        qParams = []
        self.checkValid(q, method)
        q2 = q.copy()
        del q2['table']
        ret = ''
        if method == 'PUT':
            del q2['id']
            del q2['primaryKey']
            qString = 'update %s set %s where %s=?' % (q['table'], (', ').join('%s=?' % p for p in q2.keys()), q['primaryKey'])
            qParams = [ v for k, v in q2.items() ]
            qParams.append(q[q['primaryKey']])
        elif method == 'POST':
            del q2['primaryKey']
            qString = 'insert into %s (%s) values (%s)' % (q['table'], (',').join(q2.keys()), (',').join('?' for p in q2.keys()))
            qParams = [ v for k, v in q2.items() ]
            ret = '<a href="" class="alert-link">Refresh Page</a>'
        elif method == 'DELETE':
            qString = 'delete from %s where %s=?' % (q['table'], q['primaryKey'])
            qParams = [q['id']]
            ret = 'Row deleted'
        self.db.execute(qString, qParams)
        self.db.commit()
        return ret