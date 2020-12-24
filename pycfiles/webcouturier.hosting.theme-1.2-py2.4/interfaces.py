# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/webcouturier/hosting/theme/browser/interfaces.py
# Compiled at: 2008-07-25 04:13:55
from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """
    __module__ = __name__


class IThemeTablelessSpecific(IThemeSpecific):
    """Marker interface that defines a Zope 3 skin layer.
       This one is used for tableless version only of the skin
    """
    __module__ = __name__