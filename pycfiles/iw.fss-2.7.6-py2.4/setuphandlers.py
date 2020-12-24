# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/setuphandlers.py
# Compiled at: 2008-10-23 05:55:17
from Products.CMFCore.utils import getToolByName
from iw.fss.modifier import MODIFIER_ID
from iw.fss.modifier import manage_addModifier

def thisProfileOnly(func):
    """Decorator that prevents the setup func to be used on other GS profiles.
    Usage:
    @thisProfileOnly
    def someFunc(context): ...
    """

    def wrapper(context):
        if context.readDataFile('iw.fss.txt') is None:
            return
        else:
            return func(context)
        return

    return wrapper


@thisProfileOnly
def setupVarious(context):
    """Put here various stuff that cannot be installed with generic setup"""
    portal = context.getSite()
    mtool = getToolByName(portal, 'portal_modifier')
    if MODIFIER_ID not in mtool.objectIds():
        manage_addModifier(mtool)