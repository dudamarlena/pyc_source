# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freearch/theme/browser/interfaces.py
# Compiled at: 2008-06-18 07:12:50
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "freearch Theme" theme, this interface must be its layer
       (in theme/viewlets/configure.zcml).
    """
    pass


class IFreeArchFolderTitle(IViewletManager):
    """Marker intreface for freearchFolderTitle.
        """
    pass