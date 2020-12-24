# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sqlapi.py
# Compiled at: 2018-12-16 08:49:24
# Size of source mod 2**32: 1091 bytes
import MySQLdb, sys

class sqlapi:
    __doc__ = '\n    初始化\n    '

    def __init__(self, host_str, user_str, passwd_str, db_str):
        reconnect = 10
        while reconnect > 0:
            try:
                self.conn = MySQLdb.connect(host=host_str, user=user_str, passwd=passwd_str, db=db_str, charset='utf8')
            except:
                reconnect -= 1
                print(sys.exc_info())
            else:
                self.cursor = self.conn.cursor()
                return

    def Run_Sql(self, sqlstr):
        date = -1
        try:
            date = self.cursor.execute(sqlstr)
        except:
            print(sqlstr)
            print(sys.exc_info())

        return date

    def GetOneDate(self):
        return self.cursor.fetchone()

    def GetAllDate(self, num):
        return self.cursor.fetchmany(num)

    def __del__(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()