# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/interfaces.py
# Compiled at: 2019-12-24 07:39:43
# Size of source mod 2**32: 7586 bytes
"""PyAMS_table.interfaces module

This module provides all package interfaces.
"""
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, Interface
from zope.schema import BytesLine, Int, List, TextLine
__docformat__ = 'restructuredtext'

class IValues(Interface):
    __doc__ = 'Table value adapter.'
    values = Attribute('Iterable table row data sequence.')


class ITable(IContentProvider):
    __doc__ = 'Table provider'
    column_counter = Int(title='Column counter', description='Column counter', default=0)
    column_index_by_id = Attribute('Dict of column index number by id')
    column_by_name = Attribute('Dict of columns by name')
    columns = Attribute('Sequence of columns')
    rows = Attribute('Sequence of rows')
    selected_items = Attribute('Sequence of selected items')
    prefix = BytesLine(title='Prefix', description='The prefix of the table used to uniquely identify it.', default=b'table')
    css_classes = Attribute('Dict of element name and CSS classes')
    css_class_even = TextLine(title='Even css row class', description='CSS class for even rows.', default='even', required=False)
    css_class_odd = TextLine(title='Odd css row class', description='CSS class for odd rows.', default='odd', required=False)
    css_class_selected = TextLine(title='Selected css row class', description='CSS class for selected rows.', default='selected', required=False)
    sort_on = Int(title='Sort on table index', description='Sort on table index', default=0)
    sort_order = TextLine(title='Sort order', description='Row sort order', default='ascending')
    reverse_sort_order_names = List(title='Selected css row class', description='CSS class for selected rows.', value_type=TextLine(title='Reverse sort order name', description='Reverse sort order name'), default=[
     'descending', 'reverse', 'down'], required=False)
    batch_start = Int(title='Batch start index', description='Index the batch starts with', default=0)
    batch_size = Int(title='Batch size', description='The batch size', default=50)
    start_batching_at = Int(title='Batch start size', description='The minimal size the batch starts to get used', default=50)
    values = Attribute('Iterable table row data sequence.')

    def get_css_class(self, element, css_class=None):
        """Return the css class if any or an empty string."""
        pass

    def setup_columns(self):
        """Setup table column renderer."""
        pass

    def update_columns(self):
        """Update columns."""
        pass

    def init_columns(self):
        """Initialize columns definitions used by the table"""
        pass

    def order_columns(self):
        """Order columns."""
        pass

    def setup_row(self, item):
        """Setup table row."""
        pass

    def setup_rows(self):
        """Setup table rows."""
        pass

    def get_sort_on(self):
        """Return sort on column id."""
        pass

    def get_sort_order(self):
        """Return sort order criteria."""
        pass

    def sort_rows(self):
        """Sort rows."""
        pass

    def get_batch_size(self):
        """Return the batch size."""
        pass

    def get_batch_start(self):
        """Return the batch start index."""
        pass

    def batch_rows(self):
        """Batch rows."""
        pass

    def is_selected_row(self, row):
        """Return `True for selected row."""
        pass

    def render_table(self):
        """Render the table."""
        pass

    def render_head(self):
        """Render the thead."""
        pass

    def render_head_row(self):
        """Render the table header rows."""
        pass

    def render_head_cell(self, column):
        """Setup the table header rows."""
        pass

    def render_body(self):
        """Render the table body."""
        pass

    def render_rows(self):
        """Render the table body rows."""
        pass

    def render_row(self, row, css_class=None):
        """Render the table body rows."""
        pass

    def render_cell(self, item, column, colspan=0):
        """Render a single table body cell."""
        pass

    def render(self):
        """Plain render method without keyword arguments."""
        pass


class ISequenceTable(ITable):
    __doc__ = 'Sequence table adapts a sequence as context.\n\n    This table can be used for adapting a pyams_batching.batch.Batch instance as\n    context. Batch which wraps a ResultSet sequence.\n    '


class IColumn(Interface):
    __doc__ = 'Column provider'
    id = TextLine(title='Id', description='The column id', default=None)
    colspan = Int(title='Colspan', description='The colspan value', default=0)
    weight = Int(title='Weight', description='The column weight', default=0)
    header = TextLine(title='Header name', description='The header name', default='')
    css_classes = Attribute('Dict of element name and CSS classes')

    def get_colspan(self, item):
        """Colspan value based on the given item."""
        pass

    def render_head_cell(self):
        """Render the column header label."""
        pass

    def render_cell(self, item):
        """Render the column content."""
        pass


class INoneCell(IColumn):
    __doc__ = 'None cell used for colspan.'


class IBatchProvider(IContentProvider):
    __doc__ = 'Batch content provider'

    def render_batch_link(self, batch, css_class=None):
        """Render batch links."""
        pass

    def render(self):
        """Plain render method without keyword arguments."""
        pass


class IColumnHeader(Interface):
    __doc__ = 'Multi-adapter for header rendering.'

    def update(self):
        """Override this method in subclasses if required"""
        pass

    def render(self):
        """Return the HTML output for the header

        Make sure HTML special chars are escaped.
        Override this method in subclasses"""
        pass

    def get_query_string_args(self):
        """
        Because the header will most often be used to add links for sorting the
        columns it may also be necessary to collect other query arguments from
        the request.

        The initial use case here is to maintain a search term.
        """
        pass