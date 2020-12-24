# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/sql/upsert.py
# Compiled at: 2012-10-12 07:02:39
from StringIO import StringIO
from time import sleep
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from utility import sql_connect
from command import SQLCommand

class UpsertAction(ActionCommand, SQLCommand):
    __domain__ = 'action'
    __operation__ = 'sql-upsert'
    __aliases__ = ['sqlUpsert', 'sqlUpsertAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        db = sql_connect(self._source)
        cursor = db.cursor()
        summary = StringIO('')
        (table_name, format_name, format_class) = self._read_result_metadata(self.rfile)
        summary.write(('Upsert target is table {0}\n').format(table_name))
        counter = 0
        update_count = 0
        insert_count = 0
        try:
            for (keys, fields) in self._read_rows(self.rfile, []):
                if len(keys) == 0:
                    raise CoilsException('No primary keys provided for update of SQL record.')
                (sql, values) = self._create_pk_select_from_keys(db, table_name, keys)
                cursor = db.cursor()
                try:
                    try:
                        cursor.execute(sql, values)
                        count = len(cursor.fetchall())
                    except Exception, e:
                        self.log_message(('FAILED SQL: {0} VALUES: {1}').format(unicode(sql), unicode(values)), category='error')
                        raise e

                finally:
                    cursor.close()

                if count == 0:
                    (sql, values) = self._create_insert_from_fields(db, table_name, keys, fields)
                    insert_count += 1
                elif count == 1:
                    (sql, values) = self._create_update_from_fields(db, table_name, keys, fields)
                    update_count += 1
                else:
                    self.log_message(('Primary key search returned more than one tuple.\n SQL: {0}\n VALUES: {1}').format(unicode(sql), unicode(values)), category='error')
                    raise CoilsException('Primary key search returned more than one record!')
                cursor = db.cursor()
                try:
                    try:
                        cursor.execute(sql, values)
                    except Exception, e:
                        self.log_message(('FAILED SQL: {0} VALUES: {1}').format(unicode(sql), unicode(values)), category='error')
                        raise e

                finally:
                    cursor.close()

                counter += 1
                if counter % 1000 == 0:
                    sleep(0.5)

            if self._commit == 'YES':
                db.commit()
        finally:
            summary.write(('{0} records processed.').format(counter))
            self.log_message(summary.getvalue(), category='error')
            summary = None
            db.close()

        return

    def parse_action_parameters(self):
        self._commit = self.action_parameters.get('commit', 'YES').upper()
        self._source = self.action_parameters.get('dataSource', None)
        self._keys = self.action_parameters.get('primaryKeys', '').split(',')
        if self._source is None:
            raise CoilsException('No source defined for selectAction')
        return

    def do_epilogue(self):
        pass