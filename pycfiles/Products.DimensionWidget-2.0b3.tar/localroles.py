# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/localroles.py
# Compiled at: 2009-04-26 22:17:24
from plone.app.workflow.interfaces import ISharingPageRole
from zope.interface import implements
from Products.DigestoContentTypes import DigestoContentTypesMessageFactory as _

class MetadataEditorRole(object):
    __module__ = __name__
    implements(ISharingPageRole)
    title = _('title_can_edit_metadata', default='Can edit metadata')
    required_permission = None