# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/classes/sql/singlethreadsinglecursor.py
# Compiled at: 2018-08-03 16:13:05
from threading import Thread
import Queue
from pysqlcipher import dbapi2 as sqlite
from zas_rep_tools.src.utils.custom_exceptions import ZASCursorError, ZASConnectionError
from zas_rep_tools.src.utils.debugger import p
from zas_rep_tools.src.classes.sql.basic import BasicConnection, BasicCursor
OperationalError = sqlite.OperationalError
DatabaseError = sqlite.DatabaseError
DataError = sqlite.DataError
InternalError = sqlite.InternalError
IntegrityError = sqlite.IntegrityError
NotSupportedError = sqlite.NotSupportedError
ProgrammingError = sqlite.ProgrammingError
auto_clear = True

def connect(*args, **kwargs):
    return SingleThreadSingleCursor().connect(*args, **kwargs)


class SingleThreadSingleCursor(BasicConnection):

    def __init__(self, *args, **kwargs):
        self._connection = False
        super(type(self), self).__init__(*args, **kwargs)
        self.active_cursor = False

    def cursor(self, *args, **kwargs):
        self.active_cursor = self._cursor(*args, **kwargs)
        return self.active_cursor

    def _cursor(self, *args, **kwargs):
        if not self._connection:
            raise ZASConnectionError, 'No active Connection!'
        if self.active_cursor:
            if auto_clear:
                self.clear()
            else:
                raise ZASCursorError, "Cursor is already exist! Set 'auto_clear'-Option."
        if not self.active_cursor:
            return BasicCursor(self._connection, *args, **kwargs)

    def clear(self):
        if not self.active_cursor:
            raise ZASCursorError, 'Cursor is not exist!'
        del self.active_cursor
        self.active_cursor = None
        return