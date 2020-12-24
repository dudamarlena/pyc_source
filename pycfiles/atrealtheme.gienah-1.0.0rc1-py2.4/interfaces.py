# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atrealtheme/gienah/browser/interfaces.py
# Compiled at: 2009-08-25 12:59:06
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager

class IThemeSpecific(IDefaultPloneLayer):
    """ Marker interface that defines a Zope 3 browser layer. """
    __module__ = __name__


class IAtrealThemeTopManager(IViewletManager):
    """ A viewlet manager thats sits above content and column right. """
    __module__ = __name__