# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/batch.py
# Compiled at: 2019-12-24 08:25:06
# Size of source mod 2**32: 5593 bytes
"""PyAMS_table.batch module

This module provides batch features for tables, using PyAMS_batching package.
"""
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
    __doc__ = 'Batch content provider\n\n    A batch provider is responsible for rendering the batch HTML and not for\n    batching. The batch setup is directly done in the table. A batch provider\n    get only used if the table rows is a batch.\n\n    This batch provider offers a batch presentation for a given table. The\n    batch provides different configuration options which can be overriden in\n    custom implementations:\n\n    The batch acts like this. If we have more batches than\n    (prev_batch_size + next_batch_size + 3) then the advanced batch subset is used.\n    Otherwise, we will render all batch links.\n    Note, the additional factor 3 is the placeholder for the first, current and\n    last item.\n\n    Such a batch looks like:\n\n    Renders the link for the first batch, spacers, the amount of links for\n    previous batches, the current batch link, spacers, the amount of links for\n    previous batches and the link for the last batch.\n\n    Sample for 1000 items with 100 batches with batchSize of 10 and a\n    prev_batch_size of 3 and a next_batch_size of 3:\n\n    For the first item:\n    [*1*][2][3][4] ... [100]\n\n    In the middle:\n    [1] ... [6][7][8][*9*][10][11][12] ... [100]\n\n    At the end:\n    [1] ... [97][98][99][*100*]\n    '
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