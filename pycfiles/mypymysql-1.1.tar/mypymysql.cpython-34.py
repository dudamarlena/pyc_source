# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python学习\mypymysql\mypymysql\mypymysql.py
# Compiled at: 2019-11-10 03:04:51
# Size of source mod 2**32: 1100 bytes
import pymysql

class mypymysql(object):

    def __init__(self):
        pass

    def connect(self, *args, **kwargs):
        pass

    def getConnect(self, host, user, password, token):
        conn = pymysql.connect(host, user, password, db='db_campus', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select * from tb_user where token = '%s'" % token
        cursor.execute(sql)
        one = cursor.fetchone()
        hostIP = one['host']
        port = one['port']
        username = one['name']
        password = one['password']
        conn = pymysql.connect(hostIP, user, password, db='db_campus', charset='utf8')
        return conn


if __name__ == '__main__':
    m = mypymysql()
    s = m.getConnect('127.0.0.1', 'root', '123456', 'fdsf3485fsadgaga')
    print(s)