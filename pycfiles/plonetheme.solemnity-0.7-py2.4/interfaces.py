# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/solemnity/browser/interfaces.py
# Compiled at: 2009-08-19 07:35:20
from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "Solemnity Theme" theme, this interface must be its layer
       (in solemnity/viewlets/configure.zcml).
    """
    __module__ = __name__