# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/workgroup/content/memberarea.py
# Compiled at: 2008-06-25 09:09:13
from zope.interface import alsoProvides
from Products.Archetypes.public import *
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.folder import ATBTreeFolderSchema
from Products.ATContentTypes.content.folder import ATBTreeFolder
from Products.CMFCore.utils import getToolByName
from redomino.workgroup.config import PROJECTNAME
memberarea_schema = ATBTreeFolderSchema.copy() + Schema(())

class MemberArea(ATBTreeFolder):
    __module__ = __name__
    security = ClassSecurityInfo()
    schema = memberarea_schema
    meta_type = 'MemberArea'
    portal_type = 'MemberArea'
    archetype_name = 'MemberArea'
    global_allow = 1
    allowed_content_types = ['Member']
    filter_content_types = 1


registerType(MemberArea, PROJECTNAME)