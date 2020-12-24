# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/theme/browser/interfaces.py
# Compiled at: 2009-07-01 06:06:52
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__


class IPortalWwpDate(IViewletManager):
    """A viewlet manager for pete's custom section displayed in header of rendered page  """
    __module__ = __name__


class IPortalAdBlockTop(IViewletManager):
    """A viewlet manager for pete's custom section displayed in header of rendered page  """
    __module__ = __name__