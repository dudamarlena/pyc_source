# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\db\oracle\connection.py
# Compiled at: 2016-01-14 15:12:15
DEFAULT_NLS_LANG = 'AMERICAN_AMERICA.AL32UTF8'
import os
os.environ['NLS_LANG'] = DEFAULT_NLS_LANG
import cx_Oracle

class OracleConnection(object):

    def __init__(self, info):
        self.connection = cx_Oracle.connect(info[0])
        self.setup_dbms_metadata()

    def cursor(self):
        return self.connection.cursor()

    def setup_dbms_metadata(self):
        cursor = self.connection.cursor()
        cursor.execute("\n            DECLARE\n              ncount INTEGER;\n            BEGIN\n                dbms_metadata.set_transform_param(dbms_metadata.session_transform,'SQLTERMINATOR', true);\n                SELECT count(*)    INTO ncount \n                FROM  user_objects WHERE status <> 'VALID';\n                IF ncount > 0 THEN\n                   dbms_utility.compile_schema(USER);\n                END IF;\n            END;")
        cursor.close()

    def close(self):
        self.connection.close()