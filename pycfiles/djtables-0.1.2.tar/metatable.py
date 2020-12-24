# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/adammck/projects/djtables/example/djtables/metatable.py
# Compiled at: 2010-06-09 10:01:36
from .options import TableOptions
from .column import Column

class MetaTable(type):

    def __new__(cls, name, bases, attrs):
        options_class = attrs.pop('options_class', TableOptions)
        column_class = attrs.pop('column_class', Column)
        columns = dict([ (attname, attrs.pop(attname)) for attname, value in attrs.items() if isinstance(value, column_class)
                       ])
        attrs['_meta'] = options_class(attrs.pop('Meta', None))
        obj = super(MetaTable, cls).__new__(cls, name, bases, attrs)
        for name, column in columns.items():
            column.bind_to(obj, name)

        obj._meta.columns = sorted(columns.values())
        return obj