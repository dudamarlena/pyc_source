# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/worldcookeryskin/interfaces.py
# Compiled at: 2007-02-23 15:51:20
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewletManager

class IWorldCookeryLayer(IBrowserRequest):
    """Skin layer that contains skin elements common to all
    WorldCookery applications"""
    __module__ = __name__


class IHeaders(IViewletManager):
    """Viewlets for the HTML header"""
    __module__ = __name__


class IToolbar(IViewletManager):
    """Viewlets for the toolbar (e.g. tabs and actions)"""
    __module__ = __name__


class ISidebar(IViewletManager):
    """Viewlets for the sidebar (e.g. add menu)"""
    __module__ = __name__


class IFooter(IViewletManager):
    """Viewlets for the footer (e.g. colophon)"""
    __module__ = __name__