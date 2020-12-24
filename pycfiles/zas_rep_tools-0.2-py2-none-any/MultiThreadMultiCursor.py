# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/classes/sql/MultiThreadMultiCursor.py
# Compiled at: 2018-10-09 11:23:28
import threading, Queue, inspect
from pysqlcipher import dbapi2 as sqlite
from zas_rep_tools.src.utils.custom_exceptions import ZASCursorError, ZASConnectionError
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.classes.sql.basic import BasicConnection, BasicCursor
from zas_rep_tools.src.classes.basecontent import BaseContent
OperationalError = sqlite.OperationalError
DatabaseError = sqlite.DatabaseError
DataError = sqlite.DataError
InternalError = sqlite.InternalError
IntegrityError = sqlite.IntegrityError
NotSupportedError = sqlite.NotSupportedError
ProgrammingError = sqlite.ProgrammingError
InterfaceError = sqlite.InterfaceError
auto_clear = True

def connect(*args, **kwargs):
    return MultiThreadMultiCursor(*args, **kwargs).connect(*args, **kwargs)


class MultiThreadMultiCursor(BaseContent, BasicConnection, threading.Thread):

    def __init__(self, *args, **kwargs):
        super(type(self), self).__init__(**kwargs)
        threading.Thread.__init__(self)
        self.lock_connection = threading.Lock()
        self.daemon = True
        self.start()

    def connect(self, *args, **kwargs):
        isolation_level = kwargs.get('isolation_level', None)
        check_same_thread = kwargs.get('check_same_thread', None)
        kargs = {}
        if isolation_level != None:
            kargs['isolation_level'] = isolation_level
        if check_same_thread != None:
            kargs['check_same_thread'] = check_same_thread
        if not self._connection:
            self._connection = sqlite.connect(*args, **kargs)
            return self
        else:
            raise ZASConnectionError, 'Connection is already exist!'
            return

    def _cursor(self, *args, **kwargs):
        if not self._connection:
            raise ZASConnectionError, 'No active Connection!'
        return MultiCursor(self._connection, self.lock_connection, *args, **kwargs)


class MultiCursor(BasicCursor, threading.Thread):

    def __init__(self, connection, conn_lock, *args, **kwargs):
        threading.Thread.__init__(self)
        self.connection = connection
        self.lock_connection = conn_lock
        self.cursor = self.connection.cursor(*args, **kwargs)
        self.daemon = True
        self.start()

    def execute(self, sql, *args, **kwargs):
        with self.lock_connection:
            self._check_cursor_existenz()
            self.cursor.execute(sql, *args, **kwargs)
            self.join()
            return self

    def executemany(self, sql, *args, **kwargs):
        with self.lock_connection:
            self._check_cursor_existenz()
            self.cursor.executemany(sql, *args, **kwargs)
            self.join()
            return self

    def executescript(self, sql, *args, **kwargs):
        with self.lock_connection:
            self._check_cursor_existenz()
            self.cursor.executescript(sql, *args, **kwargs)
            self.join()
            return self