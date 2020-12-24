# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\collective\threecolorstheme\setuphandlers.py
# Compiled at: 2008-10-12 05:16:06
from Products.CMFPlone.utils import getToolByName

def importFinalSteps(context):
    if context.readDataFile('collective.threecolorstheme_various.txt') is None:
        return
    site = context.getSite()
    setupTypesInfos(site)
    return


def setupTypesInfos(context):
    """
    Disallow skins contents
    after portal_types & structure install
    """
    ttool = getToolByName(context, 'portal_types')
    types = ['ThreeColorsThemeSkin', 'PhantasySkinsRepository']
    for type in types:
        fti = getattr(ttool, type, None)
        if fti:
            fti._setPropValue('global_allow', 0)

    return