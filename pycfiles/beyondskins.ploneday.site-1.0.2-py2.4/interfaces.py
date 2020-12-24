# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/beyondskins/ploneday/site/browser/interfaces.py
# Compiled at: 2009-05-13 13:33:30
from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "beyondskins_ploneday" theme, this interface must be its layer
       (in site/viewlets/configure.zcml).
    """
    __module__ = __name__