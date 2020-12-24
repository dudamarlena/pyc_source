# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ore/yui/interfaces.py
# Compiled at: 2011-01-05 03:08:18
from zope import interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewletManager

class IYUILayer(IBrowserRequest):
    """
    zope3 skin for yui
    """
    pass


class IYUIJavascript(IViewletManager):
    """
    zope3 viewlet manager for yui js
    """
    pass


class IYUICSS(IViewletManager):
    """
    zope3 css manager for yui
    """
    pass