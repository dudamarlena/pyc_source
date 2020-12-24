# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/romain/dev/buildouts/xnet4.1/src/atreal.cmfeditions.unlocker/atreal/cmfeditions/unlocker/setuphandlers.py
# Compiled at: 2011-11-08 05:01:06
from Products.CMFCore.utils import getToolByName
from atreal.cmfeditions.unlocker import UnlockerModifier

def importVarious(context):
    """
    Import various settings.

    Provisional handler that does initialization that is not yet taken
    care of by other handlers.
    """
    if context.readDataFile('unlocker_various.txt') is None:
        return
    else:
        site = context.getSite()
        portal_modifier = getToolByName(site, 'portal_modifier')
        UnlockerModifier.install(portal_modifier)
        return