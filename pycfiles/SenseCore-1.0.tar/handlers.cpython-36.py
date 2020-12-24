# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/john/Desktop/sense_core/handlers/handlers.py
# Compiled at: 2018-11-12 01:29:37
# Size of source mod 2**32: 1145 bytes
from .utils.db_utils import MysqlDB
import datetime, logging

class DatabaseHandler(logging.Handler):

    def __init__(self, db_host, db_user, db_pass, db):
        logging.Handler.__init__(self)
        self.conn = MysqlDB(host=db_host, user=db_user, password=db_pass, db=db)

    def getRemoteIP(self, param):
        res = str(param.__enter__()).split(',')[(-2)][9:-1]
        return res

    def build_table(self, db):
        sql = 'CREATE TABLE log (\n\t\t\tid  INT  AUTO_INCREMENT PRIMARY KEY,\n\t\t\tlevel  CHAR(4),\n\t\t\tcontent  VARCHAR(64),\n\t\t\tip  CHAR(16),\n\t\t\ttime datetime)'
        db.insert(sql)

    def insert2db(self, db, record):
        request = record.request
        level = record.levelname
        msg = record.getMessage()
        _ip = self.getRemoteIP(request)
        _time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sql = "INSERT INTO log (level,content,ip,time) VALUES ('%s','%s','%s','%s')" % (level, msg, _ip, _time)
        db.insert(sql)

    def emit(self, record):
        try:
            db = self.conn
            self.insert2db(db, record)
        except:
            try:
                self.build_table(db)
                self.insert2db(db, record)
            except:
                pass

    def close(self):
        self.conn.close()