# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/tests/utils.py
# Compiled at: 2018-04-05 17:11:06
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

def enable_rich_preview_behavior(portal_type):
    """Enable the behavior on the specified portal type."""
    fti = queryUtility(IDexterityFTI, name=portal_type)
    behavior = 'collective.behavior.richpreview.behaviors.IRichPreview'
    if behavior in fti.behaviors:
        return
    fti.behaviors += ('collective.behavior.richpreview.behaviors.IRichPreview', )