# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/skin/interfaces.py
# Compiled at: 2006-09-21 05:27:37
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.viewlet.interfaces import IViewletManager

class IWorldCookerySkin(IDefaultBrowserLayer):
    """Skin for the WorldCookery application"""
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