# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/trans/db_trans.py
# Compiled at: 2005-06-30 14:51:56
from odb import *
import profiler, socket
USER = 'root'
PASSWORD = ''
DATABASE = 'trans_data'

class TransStringTable(Table):
    __module__ = __name__

    def _defineRows(self):
        self.d_addColumn('string_id', kInteger, primarykey=1, autoincrement=1)
        self.d_addColumn('string', kBigString, indexed=1)


class TransLocTable(Table):
    __module__ = __name__

    def _defineRows(self):
        self.d_addColumn('loc_id', kInteger, primarykey=1, autoincrement=1)
        self.d_addColumn('string_id', kInteger, indexed=1)
        self.d_addColumn('version', kInteger, default=0)
        self.d_addColumn('filename', kVarString, 255, indexed=1)
        self.d_addColumn('location', kVarString, 255)


class TransMapTable(Table):
    __module__ = __name__

    def _defineRows(self):
        self.d_addColumn('string_id', kInteger, primarykey=1)
        self.d_addColumn('lang', kFixedString, 2, primarykey=1)
        self.d_addColumn('string', kBigString)


class DB(Database):
    __module__ = __name__

    def __init__(self, db, debug=0):
        self.db = db
        self._cursor = None
        self.debug = debug
        self.addTable('strings', 'nt_trans_strings', TransStringTable)
        self.addTable('locs', 'nt_trans_locs', TransLocTable)
        self.addTable('maps', 'nt_trans_maps', TransMapTable)
        return

    def defaultCursor(self):
        if self._cursor is None:
            if self.debug:
                self._cursor = profiler.ProfilerCursor(self.db.cursor())
            else:
                self._cursor = self.db.cursor()
        return self._cursor
        return


def trans_connect(host='localhost', debug=0):
    if host != 'localhost':
        local_name = socket.gethostname()
        if string.find(local_name, '.') == -1:
            local_name = local_name + '.neotonic.com'
        if local_name == host:
            host = 'localhost'
    if debug:
        p = profiler.Profiler('SQL', 'Connect -- %s:trans' % host)
    db = MySQLdb.connect(host=host, user=USER, passwd=PASSWORD, db=DATABASE)
    if debug:
        p.end()
    retval = DB(db, debug=debug)
    return retval