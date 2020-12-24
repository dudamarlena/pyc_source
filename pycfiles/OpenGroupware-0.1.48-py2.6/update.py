# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/sql/update.py
# Compiled at: 2012-10-12 07:02:39
from StringIO import StringIO
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from utility import sql_connect
from command import SQLCommand

class UpdateAction(ActionCommand, SQLCommand):
    __domain__ = 'action'
    __operation__ = 'sql-update'
    __aliases__ = ['sqlUpdate', 'sqlUpdateAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        db = sql_connect(self._source)
        cursor = db.cursor()
        summary = StringIO('')
        (table, format_name, format_class) = self._read_result_metadata(self.rfile)
        summary.write(('Update target is table "{0}"\n').format(table))
        counter = 0
        try:
            try:
                for (keys, fields) in self._read_rows(self.rfile, [], for_operation='update'):
                    if not fields:
                        continue
                    if not keys:
                        raise CoilsException('No primary keys provided for update of SQL record.')
                    (sql, values) = self._create_update_from_fields(db, table, keys, fields)
                    try:
                        cursor.execute(sql, values)
                    except Exception, e:
                        self.log_message(('FAILED SQL: {0} VALUES: {1}').format(unicode(sql), unicode(values)), category='error')
                        raise e

                    counter += 1

                if self._commit == 'YES':
                    db.commit()
            except Exception, e:
                raise e

        finally:
            summary.write(('{0} records processed.').format(counter))
            self.log_message(summary.getvalue(), category='error')
            summary = None
            cursor.close()
            db.close()

        return

    def parse_action_parameters(self):
        self._source = self.action_parameters.get('dataSource', None)
        self._keys = self.action_parameters.get('primaryKeys', '').split(',')
        self._commit = self.action_parameters.get('commit', 'YES').upper()
        if self._source is None:
            raise CoilsException('No source defined for selectAction')
        return

    def do_epilogue(self):
        pass