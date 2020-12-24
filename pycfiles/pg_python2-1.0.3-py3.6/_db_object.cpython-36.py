# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/_db_object.py
# Compiled at: 2018-06-20 09:55:01
# Size of source mod 2**32: 1046 bytes
import logging, psycopg2

class Db(object):
    params = None
    connection = None
    logger = None

    def __init__(self, params):
        self.params = params
        self._make_connection()

    def _make_connection(self):
        logging.info(self.params)
        try:
            self.connection = (psycopg2.connect)(**self.params)
        except Exception as e:
            logging.error('Error %s' % e)

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        try:
            cursor = self.connection.cursor()
            return cursor
        except Exception as err:
            logging.warning('Connection seems to have expired, remaking it')
            self._make_connection()
            cursor = self.connection.cursor()
            return cursor

    def close_cursor(self, cursor):
        cursor.close()

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        self.connection.close()