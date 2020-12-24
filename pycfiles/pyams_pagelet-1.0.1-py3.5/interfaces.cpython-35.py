# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_pagelet/interfaces.py
# Compiled at: 2020-02-20 08:01:50
# Size of source mod 2**32: 1481 bytes
"""PyAMS_pagelet.interfaces module

"""
from pyramid.interfaces import IView
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, implementer
from zope.interface.interfaces import IObjectEvent, ObjectEvent
__docformat__ = 'restructuredtext'

class IPagelet(IView):
    __doc__ = 'Pagelet interface'

    def update(self):
        """Update the pagelet data."""
        pass

    def render(self):
        """Render the pagelet content w/o o-wrap."""
        pass


class IPageletRenderer(IContentProvider):
    __doc__ = "Render a pagelet by calling it's 'render' method"


class IPageletCreatedEvent(IObjectEvent):
    __doc__ = 'Pagelet created event interface'
    request = Attribute('The request object')


@implementer(IPageletCreatedEvent)
class PageletCreatedEvent(ObjectEvent):
    __doc__ = 'Pagelet created event'

    def __init__(self, object):
        super(PageletCreatedEvent, self).__init__(object)
        self.request = object.request