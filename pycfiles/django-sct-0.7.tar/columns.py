# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/generic/advanced_object_list/columns.py
# Compiled at: 2012-03-17 12:42:14
from django.utils.safestring import mark_for_escaping
from copy import deepcopy

class Column(object):
    creation_counter = 0

    def __init__(self, type='default', label=None, filter=None, default_sortorder=None):
        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1
        self.type = type
        self.label = label
        self.filter = filter
        self.default_sortorder = default_sortorder

    def get_label(self):
        if self.label is not None:
            return self.label
        else:
            return self._get_label()

    def _get_label(self):
        pass

    def get_default_sortorder(self):
        if self.default_sortorder is not None:
            return self.default_sortorder
        else:
            return self._get_default_sortorder()

    def _get_default_sortorder(self):
        return 'asc'

    def get_value(self, object):
        value = self._get_value(object)
        if self.filter is not None:
            return self.filter(object, self, value)
        else:
            return value

    def _get_value(self, object):
        """
        subclasses should fetch the value from the object.
        they are also responsible for escaping html characters & co.
        """
        pass

    def sort_queryset(self, queryset, direction):
        """
        should apply the sorting to the given queryset and return it.
        """
        return self.sort_list(queryset, direction)

    def new_configure(self, config):
        """
        Returns a new instance of this column with the specified configuration.
        """
        col = deepcopy(self)
        col.configure(config)
        return col

    def configure(self, config):
        self.config = config

    def sort_list(self, sortlist, direction):
        return sortlist

    def is_sortable(self):
        return False


class AttributeColumn(Column):
    """
    a very simple column which simply retrieves
    the value of an attribute.
    """

    def __init__(self, attr_name, sortcolumn=None, *args, **kwargs):
        super(AttributeColumn, self).__init__(*args, **kwargs)
        self.attr_name = attr_name
        self.attr_path = attr_name.split('.')
        self.sortcolumn = sortcolumn

    def _get_label(self):
        return self.attr_name

    def _get_value(self, object):
        value = object
        for entry in self.attr_path:
            value = getattr(value, entry)
            if callable(value):
                value = value()

        return value

    def sort_queryset(self, queryset, direction):
        if direction == 'desc':
            return queryset.order_by('-' + self.sortcolumn)
        return queryset.order_by(self.sortcolumn)

    def is_sortable(self):
        return self.sortcolumn is not None