# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/tables/presence_lookup_table.py
# Compiled at: 2012-10-12 07:02:39
import logging, inspect, yaml, uuid
from coils.foundation import *
from coils.core import *
from table import Table

class PresenceLookupTable(Table):

    def __repr__(self):
        return ('<PresenceLookupTable name="{0}" count="{1}"/>').format(self.name, len(self.c['values']))

    def set_description(self, description):
        self.c = description
        if 'values' not in self.c:
            raise CoilsException('PresenceLookupTable does not contain the required "values" attribute.')
        if not isinstance(self.c['values'], list):
            raise CoilsException(('"value" attribute of PresenceLookupTable is a "{0}" and must be a "list".').format(type(self.c['values'])))
        if 'returnValueForTrue' not in self.c:
            raise CoilsException('PresenceLookupTable does not contain the required "returnValueForTrue" attribute.')
        if 'returnValueForFalse' not in self.c:
            raise CoilsException('PresenceLookupTable does not contain the required "returnValueForFalse" attribute.')

    def lookup_value(self, value):
        if value in self.c['values']:
            return self.c['returnValueForTrue']
        else:
            return self.c['returnValueForFalse']