# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/content/ATSuccessStoryFolder.py
# Compiled at: 2015-12-17 03:21:31
__author__ = 'Franco Pellegrini <frapell@menttes.com>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.ATSuccessStory.config import *
schema = Schema(())
ATSuccessStoryFolder_schema = getattr(ATFolder, 'schema', Schema(())).copy() + schema.copy()

class ATSuccessStoryFolder(ATFolder):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IATSuccessStoryFolder)
    meta_type = 'ATSuccessStoryFolder'
    _at_rename_after_creation = True
    schema = ATSuccessStoryFolder_schema


registerType(ATSuccessStoryFolder, PROJECTNAME)