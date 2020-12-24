# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/format/simple_filter.py
# Compiled at: 2012-10-12 07:02:39
import string
from StringIO import StringIO
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class SimpleFilter(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'simple-filter'
    __aliases__ = ['simpleFilter', 'simpleFilterAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        summary = StringIO('')
        self._row_in = 0
        self._row_out = 0
        try:
            StandardXML.Filter_Rows(self._rfile, self._wfile, callback=self.callback)
        finally:
            summary.write(('\n  Rows input = {0}, Rows output = {1}').format(self._row_in, self._row_out))
            self.log_message(summary.getvalue(), category='info')

    def callback(self, row):
        self._row_in += 1
        (keys, fields) = StandardXML.Parse_Row(row)
        if self._field_name in keys:
            x = keys[self._field_name]
        elif self._field_name in fields:
            x = fields[self._field_name]
        else:
            raise CoilsException(('Field {0} not found in input record.').format(self._field_name))
        if self._expression == 'EQUALS':
            if x == self._compare_value:
                self._row_out += 1
                return True
            return False
        if self._expression == 'NOT-EQUALS':
            if x != self._compare_value:
                self._row_out += 1
                return True
            return False
        raise CoilsException(('Unknown comparision expression: {0}').format(self._compare_value))

    def parse_action_parameters(self):
        self._field_name = self._params.get('fieldName', None)
        self._expression = self._params.get('expression', 'EQUALS').upper()
        self._cast_as = self._params.get('castAs', 'STRING').upper()
        self._compare_value = self._params.get('compareValue', None)
        if self._field_name is None:
            raise CoilsException('No field name specified for comparison.')
        if self._compare_value is None:
            raise CoilsException('No comparison expression specified')
        if self._cast_as == 'INTEGER':
            self._compare_value = int(self._compare_value)
        elif self._cast_as == 'FLOAT':
            self._compare_value = float(self._compare_value)
        elif self._cast_as == 'UNICODE':
            self._compare_value = unicode(self._compare_value)
        return