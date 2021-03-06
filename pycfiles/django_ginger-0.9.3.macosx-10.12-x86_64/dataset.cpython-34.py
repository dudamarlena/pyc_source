# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/dataset.py
# Compiled at: 2016-03-04 14:22:32
# Size of source mod 2**32: 11253 bytes
from __future__ import division
import itertools, inspect, weakref
from collections import OrderedDict
import collections
from django.utils import six
from django.utils.safestring import mark_safe
from ginger import ui
from ginger.utils import get_url_with_modified_params
__all__ = [
 'Column', 'GingerDataSet']

class Column(object):
    _Column__position = 1

    def __init__(self, label=None, kind=None, hidden=False, attr=None, sortable=True, linkable=False, reverse=False):
        self._Column__position += 1
        Column._Column__position += 1
        self.label = label
        self.kind = kind
        self.attr = attr
        self.hidden = hidden
        self.sortable = sortable
        self.linkable = linkable
        self.reverse = reverse

    @property
    def position(self):
        return self._Column__position

    @property
    def display_label(self):
        return (self.label or self.name).capitalize()


class BoundColumn(object):

    def __init__(self, schema, name, position, column):
        self.schema = schema
        self.column = column
        self.name = name
        self.position = position
        self.hidden = column.hidden

    def is_hidden(self):
        return self.hidden

    def toggle(self):
        if self.is_hidden():
            return self.show()
        return self.hide()

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    @property
    def reverse(self):
        return self.column.reverse

    @property
    def linkable(self):
        return self.column.linkable

    @property
    def sortable(self):
        return self.column.sortable

    @property
    def kind(self):
        return self.column.kind

    @property
    def attr(self):
        return self.column.attr or self.name

    @property
    def label(self):
        return self.column.label or self.name.capitalize()

    def __iter__(self):
        pos = self.position
        data = self.schema
        for row in data:
            yield row[pos]

    def __len__(self):
        return len(self.schema)

    def __getitem__(self, item):
        if type(item) == slice:
            return itertools.islice(self, item.start)
        return next(itertools.dropwhile(lambda i, _: i < item, enumerate(self)))

    def to_json(self):
        return {'name': self.name, 
         'position': self.position, 
         'kind': self.kind}

    def sort(self, key=None, reverse=False):
        i = self.position
        self.schema.rows.sort(reverse=reverse, key=--- This code section failed: ---

 L. 110         0  LOAD_DEREF               'key'
                3  LOAD_CONST               None
                6  COMPARE_OP               is-not
                9  POP_JUMP_IF_FALSE    26  'to 26'
               12  LOAD_DEREF               'key'
               15  LOAD_FAST                'row'
               18  LOAD_DEREF               'i'
               21  BINARY_SUBSCR    
               22  CALL_FUNCTION_1       1  '1 positional, 0 named'
               25  RETURN_END_IF_LAMBDA
             26_0  COME_FROM             9  '9'
               26  LOAD_FAST                'row'
               29  LOAD_DEREF               'i'
               32  BINARY_SUBSCR    
               33  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
)

    def __repr__(self):
        return 'BoundColumn<name: %s, position:  %s>' % (self.name, self.position)


class DataRow(object):
    _DataRow__inited = False

    def __init__(self, owner, obj, aggregate=False):
        self.obj = obj
        self._data = None
        self.owner = weakref.ref(owner)
        self.is_aggregate = aggregate
        self._DataRow__inited = True

    @property
    def schema(self):
        return self.owner()._get_schema()

    def prepare_attr(self, obj, attr):
        parts = attr.split('__')
        while parts:
            key = parts.pop(0)
            if isinstance(obj, collections.Mapping):
                obj = obj[key]
            else:
                obj = getattr(obj, key)

        return obj

    @property
    def data(self):
        obj = self.obj
        if self._data is None:
            schema = self.owner()._get_schema()
            if not inspect.isgenerator(obj) and not isinstance(obj, collections.Sequence):
                result = []
                for column in schema.columns:
                    attr = column.attr or column.name
                    try:
                        method = getattr(schema, 'prepare_%s' % column.name)
                    except AttributeError:
                        value = self.prepare_attr(obj, attr)
                    else:
                        value = method(obj)
                    result.append(value)

            else:
                result = obj
            self._data = result
        return self._data

    @property
    def columns(self):
        return self.owner()._get_schema().columns

    def items(self):
        return self.cells(columns=True)

    def cells(self, columns=False):
        cols = self.columns.visible()
        formatter = self.owner()._format_cell
        data = self.data
        for col in cols:
            i = col.position
            value = mark_safe(formatter(data[i], i, self))
            yield (col, value) if columns else value

    @property
    def object(self):
        return self.obj

    def __getitem__(self, item):
        return getattr(self.obj, item)

    def __getattr__(self, item):
        col = self.columns[item]
        return self.data[col.position]

    def __setattr__(self, key, value):
        if not self._DataRow__inited or key in self.__dict__:
            self.__dict__[key] = value
        else:
            col = self.columns[key]
            data = list(self.data)
            data[col.position] = value
            self.__dict__['_data'] = tuple(data)

    def __iter__(self):
        """
        iterates over non-hidden columns only
        """
        for col in self.columns.visible():
            yield self.data[col.position]

    def __len__(self):
        return len(self.columns.visible())

    def __getitem__(self, item):
        col = self.columns[item]
        return self.data[col.position]

    def to_json(self):
        return self.data


class DataSetBase(object):

    def __init__(self):
        self._DataSetBase__rows = []
        self.object_list = None

    def _get_schema(self):
        raise NotImplementedError

    @property
    def schema(self):
        return self._get_schema()

    @property
    def rows(self):
        return self._DataSetBase__rows

    def sort(self, *args, **kwargs):
        self.rows.sort(*args, **kwargs)

    def _format_cell(self, i, value):
        raise NotImplementedError

    def empty_row(self):
        data = [
         None] * len(self._get_schema().columns)
        return self.append(data)

    def append(self, data):
        row = self._make_row(data)
        self.rows.append(row)
        return row

    def extend(self, items):
        self.object_list = items
        for d in items:
            self.append(d)

    def insert(self, i, data):
        row = self._make_row(data)
        self.rows.insert(i, row)

    def _make_row(self, obj):
        row_class = self.schema.datarow_class
        if isinstance(obj, row_class):
            return obj
        return row_class(self, obj)

    def to_json(self):
        return self.rows

    def __getitem__(self, item):
        return self.rows[item]

    def __iter__(self):
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)


class DataAggregates(DataSetBase):

    def __init__(self, schema):
        super(DataAggregates, self).__init__()
        self._schema = weakref.ref(schema)

    def _format_cell(self, *args, **kwargs):
        return self.schema._format_cell(*args, **kwargs)

    def _get_schema(self):
        return self._schema()

    def _make_row(self, obj):
        row = super(DataAggregates, self)._make_row(obj)
        row.is_aggregate = True
        return row


class DictList(list):

    def __getitem__(self, item):
        if isinstance(item, six.string_types):
            try:
                return next(col for col in self if item == col.name)
            except StopIteration:
                raise KeyError('%r is not a key' % item)

        return super(DictList, self).__getitem__(item)

    def visible(self):
        return [col for col in self if not col.is_hidden()]


class GingerDataSet(DataSetBase):
    __doc__ = '\n    List of tuples\n    '
    datarow_class = DataRow

    def __init__(self, object_list=None):
        super(GingerDataSet, self).__init__()
        self._GingerDataSet__columns = self.setup_columns()
        self.aggregates = DataAggregates(self)
        if object_list:
            self.extend(object_list)

    def row_css_class(self, *args):
        pass

    def cell_css_class(self, *args):
        pass

    def is_paginated(self):
        return hasattr(self.object_list, 'paginator')

    def _get_schema(self):
        return self

    @classmethod
    def get_column_dict(cls):
        values = sorted(inspect.getmembers(cls, lambda value: isinstance(value, Column)), key=lambda val: val[1].position)
        for name, col in values:
            col.name = name

        return OrderedDict(values)

    def setup_columns(self):
        column_dict = self.get_column_dict()
        result = DictList()
        for i, (name, column) in enumerate(six.iteritems(column_dict)):
            col = BoundColumn(self, name, i, column)
            result.append(col)

        return result

    @property
    def columns(self):
        return self._GingerDataSet__columns

    def _format_cell(self, value, index, row):
        column = self.columns[index]
        suffixes = (column.name, column.kind)
        for suffix in suffixes:
            func = getattr(self, 'render_%s' % suffix, None)
            if func:
                return func(value, index, row)

        if value is not None:
            return six.text_type(value)
        return ''

    def build_links(self, request):
        data = request.GET
        sort_name = getattr(self, 'sort_parameter_name', None)
        for col in self.columns.visible():
            if sort_name:
                field = self.sort_field
                code = field.get_value_for_name(col.name)
                value = data.get(sort_name, '')
                reverse = value.startswith('-')
                if reverse:
                    value = value[1:]
                is_active = code == value
                next_value = '-%s' % code if not reverse and is_active else code
                mods = {sort_name: next_value}
            else:
                is_active = False
                reverse = False
                mods = {}
            url = get_url_with_modified_params(request, mods)
            link = ui.Link(content=col.label, url=url, is_active=is_active, reverse=reverse, sortable=col.sortable)
            yield link

    def export_csv(self, response, header=False, hidden=True):
        import csv
        writer = csv.writer(response)
        columns = tuple(col for col in self.columns if hidden or not col.is_hidden())
        if header:
            writer.writerow([col.label for col in columns])
        for row in self.rows:
            writer.writerow([row[col.position] for col in columns])

    def export_xlsx(self, response, header=False, hidden=True):
        from openpyxl import Workbook
        book = Workbook(encoding='utf-8')
        columns = tuple(col for col in self.columns if hidden or not col.is_hidden())
        sheet = book.create_sheet(index=0)
        if header:
            sheet.append([col.label for col in columns])
        for row in self.rows:
            sheet.append([row[col.position] for col in columns])

        book.save(response)

    @staticmethod
    def export_formats():
        return (('csv', 'CSV'), ('xlsx', 'XLSX'))