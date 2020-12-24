# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/mysql_helper.py
# Compiled at: 2019-12-26 21:01:52
# Size of source mod 2**32: 1654 bytes
import MySQLdb
from clocwalk.libs.core.datatype import AttribDict

class MySQLHelper(object):

    def __init__(self, **kwargs):
        """

        :param db_path:
        :param is_create:
        """
        user = kwargs.get('user', 'root')
        password = kwargs.get('passwd', '')
        db = kwargs.get('db', 'cve_cpe')
        port = kwargs.get('port', 3306)
        self.connect = MySQLdb.connect(passwd=password, db=db, user=user, port=port)
        self.cursor = self.connect.cursor()

    def create_cpe_bulk(self, items):
        """

        :param items:
        :return:
        """
        try:
            self.cursor.executemany('INSERT INTO cpe_match (`vendor`, `product`, `version`, `update`, `cpe23uri`, `edition`, `language` , `sw_edition`, `target_sw`, `target_hw`, `other`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', items)
            self.connect.commit()
        except Exception as ex:
            try:
                import traceback
                traceback.print_exc()
            finally:
                ex = None
                del ex

    def create_cve_bulk(self, items):
        """

        :param items:
        :return:
        """
        try:
            self.cursor.executemany('INSERT INTO cve (`cve`, `cpe23uri`, `description`, `links`, `problemtype`, `year`, `cvss_v2_severity`, `cvss_v2_impactscore`, `cvss_v3_impactscore`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);', items)
            self.connect.commit()
        except Exception as ex:
            try:
                import traceback
                traceback.print_exc()
            finally:
                ex = None
                del ex