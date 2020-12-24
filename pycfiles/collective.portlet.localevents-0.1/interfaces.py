# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/frisi/instances/ritualnetz/src/collective.portlet.localevents/src/collective/portlet/localevents/interfaces.py
# Compiled at: 2015-06-20 08:14:47
"""Module where all interfaces, events and exceptions live."""
from collective.portlet.localevents import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class ICollectivePortletLocaleventsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    pass