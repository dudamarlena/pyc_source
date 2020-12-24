# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/turicas/software/pyenv/versions/rows/lib/python3.6/site-packages/rows/table.py
# Compiled at: 2019-02-14 16:10:52
# Size of source mod 2**32: 8162 bytes
from __future__ import unicode_literals
import os
from collections import OrderedDict, namedtuple
from operator import itemgetter
import six
if six.PY2:
    from collections import MutableSequence, Sized
else:
    if six.PY3:
        from collections.abc import MutableSequence, Sized

class Table(MutableSequence):

    def __init__(self, fields, meta=None):
        from rows.plugins import utils
        self.fields = OrderedDict([(utils.slug(field_name), field_type) for field_name, field_type in OrderedDict(fields).items()])
        self.Row = namedtuple('Row', self.field_names)
        self._rows = []
        self.meta = dict(meta) if meta is not None else {}

    @property
    def field_names(self):
        return list(self.fields.keys())

    @property
    def field_types(self):
        return list(self.fields.values())

    @property
    def name(self):
        """Define table name based on its metadata (filename used on import)

        If `filename` is not available, return `table1`.
        """
        from rows.plugins import utils
        name = os.path.basename(self.meta.get('filename', 'table1'))
        return utils.slug(os.path.splitext(name)[0])

    def __repr__(self):
        length = len(self._rows) if isinstance(self._rows, Sized) else '?'
        imported = ''
        if 'imported_from' in self.meta:
            imported = ' (from {})'.format(self.meta['imported_from'])
        return '<rows.Table{} {} fields, {} rows>'.format(imported, len(self.fields), length)

    def _make_row(self, row):
        return [field_type.deserialize(row.get(field_name, None)) for field_name, field_type in self.fields.items()]

    def append(self, row):
        """Add a row to the table. Should be a dict"""
        self._rows.append(self._make_row(row))

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, key):
        key_type = type(key)
        if key_type == int:
            return (self.Row)(*self._rows[key])
        if key_type == slice:
            return [(self.Row)(*row) for row in self._rows[key]]
        if key_type is six.text_type:
            try:
                field_index = self.field_names.index(key)
            except ValueError:
                raise KeyError(key)

            return [row[field_index] for row in self._rows]
        raise ValueError('Unsupported key type: {}'.format(type(key).__name__))

    def __setitem__(self, key, value):
        key_type = type(key)
        if key_type == int:
            self._rows[key] = self._make_row(value)
        else:
            if key_type is six.text_type:
                from rows import fields
                from rows.plugins import utils
                values = list(value)
                if len(values) != len(self):
                    raise ValueError('Values length ({}) should be the same as Table length ({})'.format(len(values), len(self)))
                field_name = utils.slug(key)
                is_new_field = field_name not in self.field_names
                field_type = fields.detect_types([
                 field_name], [[value] for value in values])[field_name]
                self.fields[field_name] = field_type
                self.Row = namedtuple('Row', self.field_names)
                if is_new_field:
                    for row, value in zip(self._rows, values):
                        row.append(field_type.deserialize(value))

                else:
                    field_index = self.field_names.index(field_name)
                    for row, value in zip(self._rows, values):
                        row[field_index] = field_type.deserialize(value)

            else:
                raise ValueError('Unsupported key type: {}'.format(type(key).__name__))

    def __delitem__(self, key):
        key_type = type(key)
        if key_type == int:
            del self._rows[key]
        else:
            if key_type is six.text_type:
                try:
                    field_index = self.field_names.index(key)
                except ValueError:
                    raise KeyError(key)

                del self.fields[key]
                self.Row = namedtuple('Row', self.field_names)
                for row in self._rows:
                    row.pop(field_index)

            else:
                raise ValueError('Unsupported key type: {}'.format(type(key).__name__))

    def insert(self, index, row):
        self._rows.insert(index, self._make_row(row))

    def __radd__(self, other):
        if other == 0:
            return self
        raise ValueError()

    def __iadd__(self, other):
        return self + other

    def __add__(self, other):
        if other == 0:
            return self
        else:
            if not isinstance(self, type(other)) or self.fields != other.fields:
                raise ValueError('Tables have incompatible fields')
            else:
                table = Table(fields=(self.fields))
                table._rows = self._rows + other._rows
            return table

    def order_by(self, key):
        reverse = False
        if key.startswith('-'):
            key = key[1:]
            reverse = True
        field_names = self.field_names
        if key not in field_names:
            raise ValueError('Field "{}" does not exist'.format(key))
        key_index = field_names.index(key)
        self._rows.sort(key=(itemgetter(key_index)), reverse=reverse)


class FlexibleTable(Table):

    def __init__(self, fields=None, meta=None):
        if fields is None:
            fields = {}
        super(FlexibleTable, self).__init__(fields, meta)

    def __getitem__(self, key):
        if isinstance(key, int):
            return (self.Row)(**self._rows[key])
        if isinstance(key, slice):
            return [(self.Row)(**row) for row in self._rows[key]]
        raise ValueError('Unsupported key type: {}'.format(type(key).__name__))

    def _add_field(self, field_name, field_type):
        self.fields[field_name] = field_type
        self.Row = namedtuple('Row', self.field_names)

    def _make_row(self, row):
        from rows import fields
        for field_name in row.keys():
            if field_name not in self.field_names:
                self._add_field(field_name, fields.identify_type(row[field_name]))

        return {field_name:field_type.deserialize(row.get(field_name, None)) for field_name, field_type in self.fields.items()}

    def insert(self, index, row):
        self._rows.insert(index, self._make_row(row))

    def __setitem__(self, key, value):
        self._rows[key] = self._make_row(value)

    def append(self, row):
        """Add a row to the table. Should be a dict"""
        self._rows.append(self._make_row(row))