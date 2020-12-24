# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/frisi/instances/ritualnetz/src/collective.portlet.localevents/src/collective/portlet/localevents/interfaces.py
# Compiled at: 2015-06-20 08:14:47
__doc__ = 'Module where all interfaces, events and exceptions live.'
from collective.portlet.localevents import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class ICollectivePortletLocaleventsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""