# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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