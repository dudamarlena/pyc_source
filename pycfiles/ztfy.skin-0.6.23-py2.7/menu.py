# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/menu.py
# Compiled at: 2013-03-15 02:56:49
__docformat__ = 'restructuredtext'
from zope.publisher.interfaces.browser import IBrowserSkinType
from ztfy.skin.interfaces import IDialogMenu, ISkinnable
from z3c.menu.simple.menu import ContextMenuItem
from zope.component import queryUtility
from zope.interface import implements
from ztfy.utils.traversing import getParent
from ztfy.skin import _

class MenuItem(ContextMenuItem):
    """Default menu item"""

    @property
    def css(self):
        css = getattr(self, 'cssClass', '')
        if self.selected:
            css += ' ' + self.activeCSS
        else:
            css += ' ' + self.inActiveCSS
        if self.title.strip().startswith('::'):
            css += ' submenu'
        return css

    @property
    def selected(self):
        return self.request.getURL().endswith('/' + self.viewURL)


class SkinTargetMenuItem(MenuItem):
    """Customized menu item for specific skin targets"""
    skin = None

    def render(self):
        skinnable = getParent(self.context, ISkinnable)
        if skinnable is None:
            return ''
        else:
            skin_name = skinnable.getSkin()
            if skin_name is None:
                return ''
            skin = queryUtility(IBrowserSkinType, skin_name)
            if skin is self.skin or skin.extends(self.skin):
                return super(SkinTargetMenuItem, self).render()
            return ''
            return


class JsMenuItem(MenuItem):
    """Customized menu item with javascript link URL"""

    @property
    def url(self):
        return self.viewURL


class SkinTargetJsMenuItem(JsMenuItem):
    """Customized JS menu item for specific skin targets"""
    skin = None

    def render(self):
        skinnable = getParent(self.context, ISkinnable)
        if skinnable is None:
            return ''
        else:
            skin_name = skinnable.getSkin()
            if skin_name is None:
                return ''
            skin = queryUtility(IBrowserSkinType, skin_name)
            if skin is self.skin or skin.extends(self.skin):
                return super(SkinTargetJsMenuItem, self).render()
            return ''
            return


class DialogMenuItem(JsMenuItem):
    """Customized javascript menu item used to open a dialog"""
    implements(IDialogMenu)
    target = None

    def render(self):
        result = super(DialogMenuItem, self).render()
        if result and self.target is not None:
            for resource in self.target.resources:
                resource.need()

        return result


class SkinTargetDialogMenuItem(SkinTargetJsMenuItem):
    """Customized JS dialog menu item for specific skin targets"""
    implements(IDialogMenu)
    target = None

    def render(self):
        result = super(SkinTargetJsMenuItem, self).render()
        if result and self.target is not None:
            for resource in self.target.resources:
                resource.need()

        return result


class PropertiesMenuItem(MenuItem):
    """Default properties menu item"""
    title = _('Properties')