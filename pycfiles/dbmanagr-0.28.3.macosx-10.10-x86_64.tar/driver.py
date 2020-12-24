# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/driver/sqlite/driver.py
# Compiled at: 2015-10-11 07:17:06
import logging
from dbmanagr.logger import LogWith
from dbmanagr.options import restriction, FileOptionsParser
from dbmanagr.driver import DatabaseDriver
logger = logging.getLogger(__name__)

class SQLiteDriver(DatabaseDriver):

    @LogWith(logger)
    def restriction(self, *args):
        return restriction(*args)

    def statement_activity(self, con):
        return []

    def __repr__(self):
        return str(self.__dict__)


class SQLiteOptionsParser(FileOptionsParser):

    def create_driver(self):
        return SQLiteDriver()