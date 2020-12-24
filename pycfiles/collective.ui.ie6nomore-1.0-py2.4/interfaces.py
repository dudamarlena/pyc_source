# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/collective/ui/ie6nomore/browser/interfaces.py
# Compiled at: 2009-08-04 23:53:08
from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "ie6nomore" theme, this interface must be its layer
       (in ie6nomore/viewlets/configure.zcml).
    """
    __module__ = __name__