# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymysql_sa/pymysql_dialect.py
# Compiled at: 2010-12-01 11:25:44
import pymysql
from sqlalchemy.dialects.mysql.mysqldb import MySQLDialect_mysqldb

class MySQLDialect_pymysql(MySQLDialect_mysqldb):
    driver = 'pymysql'

    @classmethod
    def dbapi(cls):
        return __import__('pymysql')

    def create_connect_args(self, url):
        opts = url.translate_connect_args(database='db', username='user', password='passwd')
        opts.update(url.query)
        util.coerce_kw_type(opts, 'compress', bool)
        util.coerce_kw_type(opts, 'connect_timeout', int)
        util.coerce_kw_type(opts, 'client_flag', int)
        util.coerce_kw_type(opts, 'local_infile', int)
        util.coerce_kw_type(opts, 'use_unicode', bool)
        util.coerce_kw_type(opts, 'charset', str)
        ssl = {}
        for key in ['ssl_ca', 'ssl_key', 'ssl_cert', 'ssl_capath', 'ssl_cipher']:
            if key in opts:
                ssl[key[4:]] = opts[key]
                util.coerce_kw_type(ssl, key[4:], str)
                del opts[key]

        if ssl:
            opts['ssl'] = ssl
        client_flag = opts.get('client_flag', 0)
        if self.dbapi is not None:
            try:
                from pymysql.constants import CLIENT as CLIENT_FLAGS
                client_flag |= CLIENT_FLAGS.FOUND_ROWS
            except:
                pass
            else:
                opts['client_flag'] = client_flag
        return [[], opts]


dialect = MySQLDialect_pymysql