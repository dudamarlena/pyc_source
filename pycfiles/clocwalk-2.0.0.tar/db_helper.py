# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/db_helper.py
# Compiled at: 2019-12-11 03:15:39
import sqlite3, os
from clocwalk.libs.core.datatype import AttribDict

class DBHelper(object):

    def __init__(self, db_path, is_create=False):
        """

        :param db_path:
        :param is_create:
        """
        if not os.path.isfile(db_path) and not is_create:
            raise IOError(("'{0}' file does not exist.").format(db_path))
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_cpe_table(self):
        """

        :return:
        """
        try:
            if self.cursor:
                self.cursor.executescript('CREATE TABLE cpe_match (\n                   `vendor` TEXT,\n                   `product` TEXT,\n                   `version` TEXT,\n                   `update` TEXT,\n                   `cpe23uri` TEXT,\n                   `version_start_including` TEXT,\n                   `version_end_including` TEXT,\n                   `version_start_excluding` TEXT,\n                   `version_end_excluding` TEXT\n               );\n               CREATE INDEX "cpe23uri" ON "cpe_match" ( "cpe23uri"  );\n               ')
        except Exception as ex:
            import traceback
            traceback.print_exc()

    def create_cve_table(self):
        """

        :return:
        """
        try:
            if self.cursor:
                self.cursor.executescript('CREATE TABLE cve (\n                   `cve` TEXT,  \n                   `cpe23uri` TEXT,  \n                   `description` TEXT,\n                   `links` TEXT,\n                   `cvss_v2_severity` TEXT,\n                   `cvss_v2_impactscore` TEXT,\n                   `cvss_v3_impactscore` TEXT\n\n               );\n               CREATE INDEX "cve_cpe23uri" ON "cve" ("cpe23uri", "cve");\n               ')
        except Exception as ex:
            pass

    def create_cnvd_table(self):
        """

        :return:
        """
        try:
            if self.cursor:
                self.cursor.execute('CREATE TABLE cnvd (\n                   `cnvd` TEXT,\n                   `description` TEXT,\n                   `risk` TEXT,\n                   `links` TEXT\n\n               );')
        except Exception as ex:
            pass

    def create_cpe_entity(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        try:
            vendor = kwargs.get('vendor')
            product = kwargs.get('product')
            version = kwargs.get('version')
            update = kwargs.get('update')
            version_start_including = kwargs.get('version_start_including')
            version_end_including = kwargs.get('version_end_including')
            version_start_excluding = kwargs.get('version_start_excluding')
            version_end_excluding = kwargs.get('version_end_excluding')
            self.cursor.execute('INSERT INTO cpe_match (`vendor`, `product`, `version`, `update`, `version_start_including`, `version_end_including`, `version_start_excluding`, `version_end_excluding`) VALUES(?, ?, ?, ?, ?, ?, ?, ?);', (
             vendor, product, version, update, version_start_including, version_end_including,
             version_start_excluding, version_end_excluding))
            self.conn.commit()
        except Exception as ex:
            import traceback
            traceback.print_exc()

    def create_cpe_bulk(self, items):
        """

        :param items:
        :return:
        """
        try:
            self.cursor.executemany('INSERT INTO cpe_match (`vendor`, `product`, `version`, `update`, `cpe23uri`, `version_start_including`, `version_end_including`, `version_start_excluding`, `version_end_excluding`) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);', items)
            self.conn.commit()
        except Exception as ex:
            import traceback
            traceback.print_exc()

    def create_cve_entity(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        try:
            cve = kwargs.get('cve')
            description = kwargs.get('description')
            cpe23uri = kwargs.get('cpe23uri')
            links = kwargs.get('links')
            cvss_v2_severity = kwargs.get('cvss_v2_severity')
            cvss_v2_impactscore = kwargs.get('cvss_v2_impactscore')
            cvss_v3_impactscore = kwargs.get('cvss_v3_impactscore')
            self.cursor.execute('INSERT INTO cve (cve, cpe23uri, description, links, cvss_v2_severity,  cvss_v2_impactscore, cvss_v3_impactscore) VALUES(?, ?, ?, ?, ?, ?, ?);', (
             cve, cpe23uri, description, links, cvss_v2_severity, cvss_v2_impactscore, cvss_v3_impactscore))
            self.conn.commit()
        except Exception as ex:
            import traceback
            traceback.print_exc()

    def create_cve_bulk(self, items):
        """

        :param items:
        :return:
        """
        try:
            self.cursor.executemany('INSERT INTO cve (cve, cpe23uri, description, links, cvss_v2_severity, cvss_v2_impactscore, cvss_v3_impactscore) VALUES(?, ?, ?, ?, ?, ?, ?);', items)
            self.conn.commit()
        except Exception as ex:
            import traceback
            traceback.print_exc()

    def create_cnvd_entity(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        try:
            cnvd = kwargs.get('cnvd')
            description = kwargs.get('description')
            risk = kwargs.get('risk')
            links = kwargs.get('links')
            self.cursor.execute('INSERT INTO cnvd (cnvd, description, risk, links) VALUES(?, ?, ?, ?);', (
             cnvd, description, risk, links))
            self.conn.commit()
        except Exception as ex:
            import traceback
            traceback.print_exc()

    def create_cnvd_bulk(self, items):
        """

        :param items:
        :return:
        """
        try:
            self.cursor.executemany('INSERT INTO cnvd (cnvd, description, risk, links) VALUES(?, ?, ?, ?)', items)
            self.conn.commit()
        except Exception as ex:
            import traceback
            traceback.print_exc()

    def query_cve_set_by_cpe23uri(self, cpe23uri):
        """

        :param cpe23uri:
        :return:
        """
        result = []
        try:
            self.cursor.execute('SELECT cve, description, links, cvss_v2_severity, cvss_v2_impactscore, cvss_v3_impactscore FROM cve WHERE cpe23uri=?', (
             cpe23uri,))
            for item in self.cursor.fetchall():
                entity = AttribDict()
                entity.cve = item[0]
                entity.description = item[1]
                entity.links = item[2]
                entity.cpe23uri = cpe23uri
                entity.cvss_v2_severity = item[3]
                entity.cvss_v2_impactscore = item[4]
                entity.cvss_v3_impactscore = item[5]
                result.append(entity)

        except Exception as ex:
            import traceback
            traceback.print_exc()

        return result

    def query_cpe_set_by_product(self, product):
        """

        :param product:
        :return:
        """
        result = []
        try:
            self.cursor.execute('SELECT `vendor`, `product`, `version`, `update`, `cpe23uri`, `version_start_including`, `version_end_including`, `version_start_excluding`, `version_end_excluding` FROM cpe_match WHERE product=?', (
             product,))
            for item in self.cursor.fetchall():
                entity = AttribDict()
                entity.vendor = item[0]
                entity.product = item[1]
                entity.version = item[2]
                entity.update_v = item[3]
                entity.cpe23uri = item[4]
                entity.version_start_including = item[5]
                entity.version_end_including = item[6]
                entity.version_start_excluding = item[7]
                entity.version_end_excluding = item[8]
                result.append(entity)

        except Exception as ex:
            import traceback
            traceback.print_exc()

        return result