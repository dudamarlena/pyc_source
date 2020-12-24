# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/content/shorturlfolder.py
# Compiled at: 2010-08-19 05:10:29
"""
shorturlfolder.py

Created by Manabu Terada on 2010-08-03.
Copyright (c) 2010 CMScom. All rights reserved.
"""
from AccessControl import ClassSecurityInfo
from zope import interface
from Products.Archetypes.atapi import *
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.configuration import zconf
from c2.app.shorturl import ShortUrlMessageFactory as _
from c2.app.shorturl.content.interfaces import IShortUrlFolder
from c2.app.shorturl.config import *
schema = Schema(())
folder_schema = getattr(ATFolder, 'schema', Schema(())).copy() + schema.copy()
finalizeATCTSchema(folder_schema)

class ShortUrlFolder(ATFolder):
    """
    """
    security = ClassSecurityInfo()
    interface.implements(IShortUrlFolder)
    schema = folder_schema
    meta_type = 'ShortUrlFolder'
    _at_rename_after_creation = True


registerType(ShortUrlFolder, PROJECTNAME)