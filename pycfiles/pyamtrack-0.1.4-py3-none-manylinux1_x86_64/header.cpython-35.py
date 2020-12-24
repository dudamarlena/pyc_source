# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/header.py
# Compiled at: 2019-12-24 07:19:59
# Size of source mod 2**32: 3126 bytes
__doc__ = 'PyAMS_table.header module\n\nThis module defines columns headers.\n'
from urllib.parse import urlencode
from zope.interface import implementer
from pyams_table.interfaces import IColumnHeader
__docformat__ = 'reStructuredText'
from pyams_table import _

@implementer(IColumnHeader)
class ColumnHeader:
    """ColumnHeader"""
    _request_args = []

    def __init__(self, context, request, table, column):
        self.__parent__ = context
        self.context = context
        self.request = request
        self.table = table
        self.column = column

    def update(self):
        """Override this method in subclasses if required"""
        pass

    def render(self):
        """Override this method in subclasses"""
        return self.column.header

    def get_query_string_args(self):
        """
        Collect additional terms from the request and include in sorting column
        headers

        Perhaps this should be in separate interface only for sorting headers?

        """
        args = {}
        for key in self._request_args:
            value = self.request.params.get(key, None)
            if value:
                args.update({key: value})

        return args


class SortingColumnHeader(ColumnHeader):
    """SortingColumnHeader"""

    def render(self):
        table = self.table
        prefix = table.prefix
        col_id = self.column.id
        current_sort_id = table.get_sort_on()
        try:
            current_sort_id = int(current_sort_id)
        except ValueError:
            current_sort_id = current_sort_id.rsplit('-', 1)[(-1)]

        current_sort_order = table.get_sort_order()
        sort_id = col_id.rsplit('-', 1)[(-1)]
        sort_order = table.sort_order
        if int(sort_id) == int(current_sort_id):
            if current_sort_order in table.reverse_sort_order_names:
                sort_order = 'ascending'
        elif current_sort_order == 'ascending':
            sort_order = table.reverse_sort_order_names[0]
        args = self.get_query_string_args()
        args.update({'%s-sort-on' % prefix: col_id, '%s-sort-order' % prefix: sort_order})
        query_string = '?%s' % urlencode(sorted(args.items()))
        translate = self.request.localizer.translate
        return '<a href="%s" title="%s">%s</a>' % (
         query_string, translate(_('Sort')), translate(self.column.header))