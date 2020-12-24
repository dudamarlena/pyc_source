# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/vertica_to_mysql.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6016 bytes
import MySQLdb
from airflow.contrib.hooks.vertica_hook import VerticaHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from contextlib import closing
import unicodecsv as csv
from tempfile import NamedTemporaryFile

class VerticaToMySqlTransfer(BaseOperator):
    """VerticaToMySqlTransfer"""
    template_fields = ('sql', 'mysql_table', 'mysql_preoperator', 'mysql_postoperator')
    template_ext = ('.sql', )
    ui_color = '#a0e08c'

    @apply_defaults
    def __init__(self, sql, mysql_table, vertica_conn_id='vertica_default', mysql_conn_id='mysql_default', mysql_preoperator=None, mysql_postoperator=None, bulk_load=False, *args, **kwargs):
        (super(VerticaToMySqlTransfer, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.mysql_table = mysql_table
        self.mysql_conn_id = mysql_conn_id
        self.mysql_preoperator = mysql_preoperator
        self.mysql_postoperator = mysql_postoperator
        self.vertica_conn_id = vertica_conn_id
        self.bulk_load = bulk_load

    def execute(self, context):
        vertica = VerticaHook(vertica_conn_id=(self.vertica_conn_id))
        mysql = MySqlHook(mysql_conn_id=(self.mysql_conn_id))
        tmpfile = None
        result = None
        selected_columns = []
        count = 0
        with closing(vertica.get_conn()) as (conn):
            with closing(conn.cursor()) as (cursor):
                cursor.execute(self.sql)
                selected_columns = [d.name for d in cursor.description]
                if self.bulk_load:
                    tmpfile = NamedTemporaryFile('w')
                    self.log.info('Selecting rows from Vertica to local file %s...', tmpfile.name)
                    self.log.info(self.sql)
                    csv_writer = csv.writer(tmpfile, delimiter='\t', encoding='utf-8')
                    for row in cursor.iterate():
                        csv_writer.writerow(row)
                        count += 1

                    tmpfile.flush()
                else:
                    self.log.info('Selecting rows from Vertica...')
                    self.log.info(self.sql)
                    result = cursor.fetchall()
                    count = len(result)
                self.log.info('Selected rows from Vertica %s', count)
        if self.mysql_preoperator:
            self.log.info('Running MySQL preoperator...')
            mysql.run(self.mysql_preoperator)
        try:
            if self.bulk_load:
                self.log.info('Bulk inserting rows into MySQL...')
                with closing(mysql.get_conn()) as (conn):
                    with closing(conn.cursor()) as (cursor):
                        cursor.execute("LOAD DATA LOCAL INFILE '%s' INTO TABLE %s LINES TERMINATED BY '\r\n' (%s)" % (
                         tmpfile.name,
                         self.mysql_table,
                         ', '.join(selected_columns)))
                        conn.commit()
                tmpfile.close()
            else:
                self.log.info('Inserting rows into MySQL...')
                mysql.insert_rows(table=(self.mysql_table), rows=result,
                  target_fields=selected_columns)
            self.log.info('Inserted rows into MySQL %s', count)
        except (MySQLdb.Error, MySQLdb.Warning):
            self.log.info('Inserted rows into MySQL 0')
            raise

        if self.mysql_postoperator:
            self.log.info('Running MySQL postoperator...')
            mysql.run(self.mysql_postoperator)
        self.log.info('Done')