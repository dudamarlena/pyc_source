# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/sql/select.py
# Compiled at: 2012-10-12 07:02:39
import base64
from coils.core import *
from coils.core.logic import ActionCommand
from utility import sql_connect
FIELD_OUT_FORMAT = '<{0} dataType="{1}" isPrimaryKey="{2}" isBase64="{3}" isNull="false">{4}</{0}>'
NULL_FIELD_OUT_FORMAT = '<{0} dataType="{1}" isPrimaryKey="false" isNull="true"/>'

class SelectAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'sql-select'
    __aliases__ = ['sqlSelectAction', 'sqlSelect']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        db = sql_connect(self._source)
        cursor = db.cursor()
        cursor.execute(self._query)
        self.wfile.write('<?xml version="1.0" encoding="UTF-8"?>')
        self.wfile.write(('<ResultSet formatName="_sqlselect_" className="" tableName="{0}">').format(self._table))
        record = cursor.fetchone()
        description = []
        for x in cursor.description:
            description.append([x[0], x[1]])

        counter = 0
        while record is not None and (counter < self._limit or self._limit == -1):
            self.wfile.write('<row>')
            for i in range(0, len(record)):
                is_base64 = False
                name = description[i][0].lower()
                kind = db.get_type_from_code(description[i][1])
                if kind == 'binary':
                    is_base64 = True
                    value = base64.encodestring(record[i])
                elif isinstance(record[i], basestring):
                    try:
                        value = record[i].decode(self._codepage).encode('utf-8', 'ignore')
                        value = self.encode_text(record[i])
                    except Exception, e:
                        self.log.error(('Unable to convert value of field {0} to UTF-8 string, using base64 encoding').format(name))
                        self.log.exception(e)
                        is_base64 = True
                        value = base64.encodestring(record[i])

                elif record[i] is not None:
                    value = record[i]
                else:
                    value = None
                is_key = name in self._keys
                if value is None:
                    if is_key:
                        raise CoilsException('NULL Primary Key value detected.')
                    self.wfile.write(NULL_FIELD_OUT_FORMAT.format(name.lower(), kind.lower()))
                else:
                    self.wfile.write(FIELD_OUT_FORMAT.format(name.lower(), kind.lower(), str(is_key).lower(), str(is_base64).lower(), value))

            self.wfile.write('</row>')
            record = cursor.fetchone()
            counter += 1

        self.wfile.write('</ResultSet>')
        description = None
        cursor.close()
        db.close()
        return

    def parse_action_parameters(self):
        self._source = self.action_parameters.get('dataSource', None)
        self._query = self.action_parameters.get('queryText', None)
        self._limit = int(self.action_parameters.get('limit', 150))
        self._table = self.action_parameters.get('tableName', '_undefined_')
        self._keys = self.action_parameters.get('primaryKeys', '').split(',')
        self._codepage = self.action_parameters.get('codepage', 'utf-8')
        if self._source is None:
            raise CoilsException('No source defined for selectAction')
        if self._query is None:
            raise CoilsException('No query defined for selectAction')
        else:
            self._query = self.decode_text(self._query)
            self._query = self.process_label_substitutions(self._query)
        return

    def do_epilogue(self):
        pass