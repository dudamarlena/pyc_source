# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/Writers/DbWriter.py
# Compiled at: 2020-04-14 15:22:04
# Size of source mod 2**32: 3549 bytes
"""
Created on Mar 6, 2018

@author: jsk
"""
import sys
from DBApps.Writers.listwriter import ListWriter
from config import config
import pymysql, os, time

class DbWriter(ListWriter):
    __doc__ = '\n    Writes to a db, connection string in the dbConfig file\n    '
    dbName = ''
    dbConfigFile = ''
    monitor_interval = 50

    def __init__(self, configInfo):
        super().__init__(configInfo)
        try:
            args = self.oConfig.drsDbConfig.split(':')
            self.dbName = args[0]
            self.dbConfigFile = os.path.expanduser(args[1])
        except IndexError:
            raise IndexError('Invalid argument: Must be formatted as section:file ')

    def write_list(self, srcList):
        """
        @summary: emits a list into the configured database
        @param srcList: Comma separated list of values

        Requires self.oConfig.sproc to exist
        """
        hadBarf = False
        cfg = config.DBConfig(self.dbName, self.dbConfigFile)
        dbConnection = self.start_connect(cfg)
        with dbConnection:
            curs = dbConnection.cursor()
            total = len(srcList)
            calls = 0
            etnow = time.perf_counter()
            try:
                for aVal in srcList:
                    try:
                        aval_type = type(aVal)
                        if aval_type is str:
                            curs.callproc(self.oConfig.sproc, (aVal.strip(),))
                        if aval_type is dict or aval_type is list:
                            curs.callproc(self.oConfig.sproc, tuple(aVal))
                        if aval_type is tuple:
                            curs.callproc(self.oConfig.sproc, aVal)
                        calls += 1
                        if calls % self.monitor_interval == 0:
                            y = time.perf_counter()
                            print(' %d calls ( %3.2f %%).  Rate: %5.2f /sec' % (
                             calls, 100 * calls / total, self.monitor_interval / (y - etnow)))
                            etnow = y
                    except UnicodeEncodeError:
                        print(':{0}::{1}:'.format(aVal[0].strip(), aVal[1].strip()))
                    except Exception:
                        hadBarf = True
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print(exc_type)
                        if dbConnection is not None:
                            dbConnection.rollback()
                        raise

            finally:
                if not hadBarf:
                    dbConnection.commit()
                if curs is not None:
                    curs.close()

    def test(self):
        cfg = config.DbConfig(self.dbName, self.dbConfigFile)
        self.start_connect(cfg)

    @staticmethod
    def start_connect(cfg):
        """
        @summary: Creates the db connection from the configuration
        """
        return pymysql.connect(read_default_file=(cfg.db_cnf), read_default_group=(cfg.db_host),
          charset='utf8')