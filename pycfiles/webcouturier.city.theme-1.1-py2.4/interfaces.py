# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/webcouturier/city/theme/browser/interfaces.py
# Compiled at: 2008-06-29 10:06:05
from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer bound to a Skin
       Selection in portal_skins.
       If you need to register a viewlet only for the "Web Couturier City Theme"
       skin, this is the interface that must be used for the layer attribute
       in Theme1/browser/configure.zcml.
    """
    __module__ = __name__