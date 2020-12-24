# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/sql/insert.py
# Compiled at: 2012-10-12 07:02:39
from time import sleep
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from utility import sql_connect
from command import SQLCommand

class InsertAction(ActionCommand, SQLCommand):
    __domain__ = 'action'
    __operation__ = 'sql-insert'
    __aliases__ = ['sqlInsert', 'sqlInsertAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        db = sql_connect(self._source)
        cursor = db.cursor()
        self.log.debug('Reading metadata from input')
        (table_name, format_name, format_class) = self._read_result_metadata(self.rfile)
        self.log_message(('Table is "{0}"').format(table_name), category='info')
        counter = 0
        try:
            row_count = 0
            for (keys, fields) in self._read_rows(self.rfile, [], for_operation='insert'):
                (sql, values) = self._create_insert_from_fields(db, table_name, keys, fields)
                try:
                    cursor.execute(sql, values)
                    row_count += 1
                except Exception, e:
                    message = ('error: FAILED SQL: {0} VALUES: {1}').format(unicode(sql), unicode(values))
                    self.log_message(message, category='error')
                    raise e

                counter += 1
                if not counter % 1000:
                    sleep(0.5)

            self.log_message(('{0} records inserted to SQL connection').format(row_count), category='info')
        finally:
            cursor.close()
            db.close()

    def parse_action_parameters(self):
        self._source = self.action_parameters.get('dataSource', None)
        if self._source is None:
            raise CoilsException('No source defined for selectAction')
        return

    def do_epilogue(self):
        pass