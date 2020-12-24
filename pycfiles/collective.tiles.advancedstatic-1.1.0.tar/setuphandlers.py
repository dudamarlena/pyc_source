# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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