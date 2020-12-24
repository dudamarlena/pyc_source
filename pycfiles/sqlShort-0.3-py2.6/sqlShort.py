# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sqlShort.py
# Compiled at: 2010-09-23 05:53:17
from numpy import *

class sqlShort:

    def __init__(self, **kwarg):
        """Creates a connection. Example:
                db = sqlShort(host="sql.server.com", user="toto", passwd="secret", db="the_toto_jokes", type="mysql")
                
                Supported database types are "mysql" and "sqlite". For sqlite, only the "host" argument is considered.
                """
        self.dbtype = kwarg.pop('type', 'mysql').lower()
        if self.dbtype == 'mysql':
            import MySQLdb as db
            self.db = db.connect(**kwarg)
        elif self.dbtype == 'sqlite':
            import sqlite3 as db
            self.db = db.connect(kwarg['host'])
            self.db.create_aggregate('STD', 1, std_sqlite)
            self.db.create_function('SQRT', 1, sqrt)
        else:
            raise ValueError("'%s' database type is not handled." % self.dbtype)
        self.dbh = self.db.cursor()
        if self.dbtype == 'sqlite':
            self.db.execute('PRAGMA journal_mode=OFF;')
            self.db.execute('PRAGMA synchronous=0;')

    def __del__(self):
        self.db.commit()
        self.dbh.close()
        self.db.close()

    def query(self, sql, **kwarg):
        """Executes a SQL query.
                In case of SELECT query, a tuple of lists is returned.
                If array=True, the returned lists are numpy arrays (if the type is numeric).
                In that cas, the dtype of the array can be provided.
                """
        is_array = kwarg.pop('Array', False) or kwarg.pop('array', False)
        dtype = kwarg.pop('dtype', 'f8')
        try:
            self.dbh.execute(sql)
        except:
            print sql
            raise

        result = self.dbh.fetchall()
        description = self.dbh.description
        if description == None:
            return ()
        else:
            n = len(description)
            if len(result) == 0:
                if is_array:
                    return tuple([ array([], dtype=dtype) for i in range(n) ])
                else:
                    return tuple([ () for i in range(n) ])
            t = list()
            for i in range(n):
                t.append([])

            for row in result:
                for i in range(n):
                    t[i].append(row[i])

            if is_array:
                if self.dbtype == 'mysql':
                    for i in range(n):
                        if description[i][1] not in db.NUMBER and description[i][1] != 246:
                            continue
                        else:
                            t[i] = array(t[i], dtype=dtype)

                else:
                    numtypes = [
                     type(int()), type(float()), type(double())]
                    for i in range(n):
                        if type(t[i][0]) in numtypes:
                            t[i] = array(t[i], dtype=dtype)
                        else:
                            continue

            return tuple(t)

    def lastrowid(self):
        """Returns the last inserted id."""
        return self.dbh.lastrowid

    def make_insert(self, arg):
        """Converts a dict into an INSERT type syntax, dealing with the types.
                If a dictionnary is provided, returns: SET `key`=value, ...
                If a list of dictionnaries is given, the long INSERT syntax is used: (`key`, ...) VALUES (value, ...), (...), ...
                In that case, the list of fields is read from the keys of the first row.
                """
        if type(arg) == type(dict()):
            fields = 'SET ' + (', ').join([ '`%s`=%s' % (k, self.str(v)) for (k, v) in arg.items() ])
        elif type(arg) == type(list()):
            n = len(arg[0].keys())
            fields = '(' + (', ').join([ '`%s`' % k for k in arg[0].keys() ]) + ')'
            fields += ' VALUES '
            L = list()
            for (i, r) in enumerate(arg):
                if len(r.values()) != n:
                    print r
                    raise ValueError('On row %d, %d arguments found, %d expected.' % (i, len(r.values()), n))
                L.append('(' + (', ').join([ self.str(v) for v in r.values() ]) + ')')

            fields += (', ').join(L)
        else:
            raise TypeError('sqlShort.make_insert() argument should be dict or list (%s given).' % type(arg))
        return fields

    def str(self, v):
        """Converts a Python variable into SQL string to insert it in a query."""
        if v is None:
            return 'NULL'
        else:
            if type(v) == type(str()):
                if self.dbtype == 'mysql':
                    return '"' + db.escape_string(v) + '"'
                else:
                    return v.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
            else:
                return str(v)
            return


class std_sqlite:

    def __init__(self):
        self.x = list()

    def step(self, v):
        self.x.append(v)

    def finalize(self):
        return std(array(self.x, dtype='f8'))