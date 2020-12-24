# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/baseskin/interfaces/container.py
# Compiled at: 2014-03-09 18:14:06
__docformat__ = 'restructuredtext'
from zope.interface import Interface
from zope.schema import Text
from ztfy.baseskin import _

class IContainerBaseView(Interface):
    """Marker interface for container base view"""
    pass


class IOrderedContainerBaseView(Interface):
    """Marker interface for ordered container based view"""
    pass


class IOrderedContainerSorterColumn(Interface):
    """Marker interface for container sorter column"""
    pass


class IIdColumn(Interface):
    """Marker interface for ID column"""
    pass


class INameColumn(Interface):
    """Marker interface for name column"""
    pass


class ITitleColumn(Interface):
    """Marker interface for title column"""
    pass


class IStatusColumn(Interface):
    """Marker interface for status column"""
    pass


class IActionsColumn(Interface):
    """Marker interface for actions column"""
    pass


class IContainerTableViewTitleCell(Interface):
    """Container table view title cell adapter"""
    prefix = Text(title=_('Text displayed before title link'))
    before = Text(title=_('Text displayed before cell main text'))
    after = Text(title=_('Text displayed after cell main text'))
    suffix = Text(title=_('Text displayed after title link'))


class IContainerTableViewStatusCell(Interface):
    """Container table view status cell interface"""
    content = Text(title=_('Content of status cell'))


class IContainerTableViewActionsCell(Interface):
    """Container table view actions cell interface"""
    content = Text(title=_('Content of actions cell'))