# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klen/Projects/simpletree/simpletree/utils.py
# Compiled at: 2012-10-14 15:26:21
from django.db import connection, transaction

def commit_raw_sql(func):
    """ Execute the query returns.
    """

    def wrapper(instance, write=True):
        sql = func(instance)
        cursor = connection.cursor()
        cursor.execute(sql)
        if write:
            transaction.commit_unless_managed()

    return wrapper