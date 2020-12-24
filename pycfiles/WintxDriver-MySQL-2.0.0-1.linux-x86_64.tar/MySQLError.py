# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/drivers/MySQL/MySQLError.py
# Compiled at: 2016-03-23 14:50:18
from wintx.errors import WintxDriverError
from mysql.connector import errorcode, Error as MySQLClientError

class MySQLError(WintxDriverError):

    def __init__(self, mysql_error):
        """MySQLError class constructor
    Inputs:
      mysql_error: mysql.connector.Error instance
    """
        self.original = mysql_error

    def __str__(self):
        return self.original.msg