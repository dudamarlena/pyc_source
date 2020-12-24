# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/batch.py
# Compiled at: 2019-12-24 08:25:06
# Size of source mod 2**32: 5593 bytes
__doc__ = 'PyAMS_table.batch module\n\nThis module provides batch features for tables, using PyAMS_batching package.\n'
from pyramid.encode import urlencode
from pyramid.interfaces import IRequest
from zope.interface import Interface
from pyams_batching.batch import first_neighbours_last
from pyams_table.interfaces import IBatchProvider, ITable
from pyams_utils.adapter import adapter_config
from pyams_utils.url import absolute_url

@adapter_config(name='batch', context=(
 Interface, IRequest, ITable), provides=IBatchProvider)
class BatchProvider:
    """BatchProvider"""
    batch_items = []
    prev_batch_size = 3
    next_batch_size = 3
    batch_spacer = '...'
    _request_args = [
     '%(prefix)s-sort-on', '%(prefix)s-sort-order']

    def __init__(self, context, request, table):
        self.__parent__ = context
        self.context = context
        self.request = request
        self.table = table
        self.batch = table.rows
        self.batches = table.rows.batches

    def get_query_string_args(self):
        """Collect additional terms from the request to include in links.

        API borrowed from pyams_table.header.ColumnHeader.
        """
        args = {}
        for key in self._request_args:
            key = key % dict(prefix=self.table.prefix)
            value = self.request.params.get(key, None)
            if value:
                args.update({key: value})

        return args

    def render_batch_link(self, batch, css_class=None):
        """Render batch link"""
        args = self.get_query_string_args()
        args[self.table.prefix + '-batch-start'] = batch.start
        args[self.table.prefix + '-batch-size'] = batch.size
        query = urlencode(sorted(args.items()))
        table_url = absolute_url(self.table, self.request)
        idx = batch.index + 1
        css = ' class="%s"' % css_class
        css_class = css if css_class else ''
        return '<a href="%s?%s"%s>%s</a>' % (table_url, query, css_class, idx)

    def update(self):
        """Update batch"""
        total = self.prev_batch_size + self.next_batch_size + 3
        if self.batch.total <= total:
            self.batch_items = self.batch.batches
        else:
            self.batch_items = first_neighbours_last(self.batches, self.batch.index, self.prev_batch_size, self.next_batch_size)

    def render(self):
        """Render batch"""
        self.update()
        res = []
        append = res.append
        idx = 0
        last_idx = len(self.batch_items)
        for batch in self.batch_items:
            idx += 1
            css_classes = []
            if batch and batch == self.batch:
                css_classes.append('current')
            if idx == 1:
                css_classes.append('first')
            if idx == last_idx:
                css_classes.append('last')
            if css_classes:
                css = ' '.join(css_classes)
            else:
                css = None
            if batch is None:
                append(self.batch_spacer)
            elif idx == 1:
                append(self.render_batch_link(batch, css))
            else:
                if batch == self.batch:
                    append(self.render_batch_link(batch, css))
                else:
                    if idx == last_idx:
                        append(self.render_batch_link(batch, css))
                    else:
                        append(self.render_batch_link(batch))

        return '\n'.join(res)