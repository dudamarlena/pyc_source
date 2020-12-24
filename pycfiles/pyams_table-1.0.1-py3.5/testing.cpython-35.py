# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/testing.py
# Compiled at: 2019-12-24 08:34:41
# Size of source mod 2**32: 3425 bytes
"""PyAMS_table.testing module

This module provides testing helpers.
"""
from datetime import datetime
from pyramid.interfaces import IRequest
from zope.container.btree import BTreeContainer
from zope.container.contained import Contained
from zope.container.interfaces import IContainer
from zope.container.ordered import OrderedContainer as BaseOrderedContainer
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import Interface, implementer
from pyams_table.column import Column, add_column
from pyams_table.interfaces import ISequenceTable, ITable, IValues
from pyams_table.table import Table
from pyams_table.value import ValuesForContainer, ValuesForSequence
__docformat__ = 'reStructuredText'

class TitleColumn(Column):
    __doc__ = 'Title column'
    weight = 10
    header = 'Title'

    def render_cell(self, item):
        """Render cell"""
        return 'Title: %s' % item.title


class NumberColumn(Column):
    __doc__ = 'Number column'
    header = 'Number'
    weight = 20

    def get_sort_key(self, item):
        """Get item sort key"""
        return item.number

    def render_cell(self, item):
        """Render column cell"""
        return 'number: %s' % item.number


class Container(BTreeContainer):
    __doc__ = 'Sample container'
    __name__ = 'container'


class OrderedContainer(BaseOrderedContainer):
    __doc__ = 'Sample container.'
    __name__ = 'container'


class Content(Contained):
    __doc__ = 'Sample content'

    def __init__(self, title, number):
        self.title = title
        self.number = number


class SimpleTable(Table):
    __doc__ = 'Simple testing table'

    def setup_columns(self):
        return [
         add_column(self, TitleColumn, 'title', cell_renderer=cell_renderer, head_cell_renderer=head_cell_renderer, weight=1),
         add_column(self, NumberColumn, name='number', weight=2, header='Number')]


def head_cell_renderer():
    """Head cell renderer"""
    return 'My items'


def cell_renderer(item):
    """Simple cell renderer"""
    return '%s item' % item.title


@implementer(IZopeDublinCore)
class DublinCoreAdapterStub:
    __doc__ = 'Dublin core adapter stub.'

    def __init__(self, context):
        pass

    title = 'faux title'
    size = 1024
    created = datetime(2001, 1, 1, 1, 1, 1)
    modified = datetime(2002, 2, 2, 2, 2, 2)


def setup_adapters(registry):
    """Adapters registry"""
    registry.registerAdapter(ValuesForContainer, (
     IContainer, IRequest, ITable), provided=IValues)
    registry.registerAdapter(ValuesForSequence, (
     Interface, IRequest, ISequenceTable), provided=IValues)
    registry.registerAdapter(DublinCoreAdapterStub, (
     Interface,), provided=IZopeDublinCore)