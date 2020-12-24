# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/webcouturier/icompany/theme/browser/interfaces.py
# Compiled at: 2008-04-30 11:18:20
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer bound to a Skin
       Selection in portal_skins.
       If you need to register a viewlet only for the "Web Couturier iCompany Theme"
       skin, this is the interface that must be used for the layer attribute
       in webcouturier.icompany.theme/browser/configure.zcml.
    """
    __module__ = __name__


class ISubmenuViewlet(Interface):
    """ Marker interface.
        Allows to render menu of sublevels with depth = 1 for current
        section. Renders as a submenu in global navigation.
    """
    __module__ = __name__

    def getSubmenu(self, selected_id=''):
        """Get the submenu tree for selected tab"""
        pass