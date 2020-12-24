# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\collective\threecolorstheme\content\skin.py
# Compiled at: 2008-10-12 05:16:06
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFCore import permissions as CCP
from Products.CMFPlone.utils import getToolByName
from Products.Archetypes.public import *
from collective.threecolorstheme.interfaces import IThreeColorsThemeSkin
from schema import ThreeColorsThemeSkinSchema
from collective.threecolorstheme.config import PROJECTNAME
from collective.phantasy.atphantasy.content.skin import PhantasySkin

class ThreeColorsThemeSkin(PhantasySkin):
    """ThreeColorsTheme Skin"""
    __module__ = __name__
    portal_type = meta_type = 'ThreeColorsThemeSkin'
    archetype_name = 'Dynamic Skin'
    global_allow = True
    schema = ThreeColorsThemeSkinSchema
    implements(IThreeColorsThemeSkin)
    security = ClassSecurityInfo()
    security.declareProtected(CCP.ModifyPortalContent, 'setLeadingColor')

    def setLeadingColor(self, value, **kwargs):
        fields = []
        fields.append(self.getField('contentViewBorderColor'))
        fields.append(self.getField('linkColor'))
        fields.append(self.getField('contentViewFontColor'))
        fields.append(self.getField('notifyBorderColor'))
        fields.append(self.getField('discreetColor'))
        fields.append(self.getField('leadingColor'))
        for field in fields:
            field.set(self, value, **kwargs)

    security.declareProtected(CCP.ModifyPortalContent, 'setLightColor2')

    def setLightColor2(self, value, **kwargs):
        fields = []
        fields.append(self.getField('contentViewBackgroundColor'))
        fields.append(self.getField('evenRowBackgroundColor'))
        fields.append(self.getField('globalBackgroundColor'))
        fields.append(self.getField('globalBorderColor'))
        fields.append(self.getField('globalFontColor'))
        fields.append(self.getField('lightColor2'))
        for field in fields:
            field.set(self, value, **kwargs)

    security.declareProtected(CCP.ModifyPortalContent, 'setLightColor1')

    def setLightColor1(self, value, **kwargs):
        fields = []
        fields.append(self.getField('notifyBackgroundColor'))
        fields.append(self.getField('lightColor1'))
        for field in fields:
            field.set(self, value, **kwargs)


registerType(ThreeColorsThemeSkin, PROJECTNAME)