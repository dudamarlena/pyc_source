# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Organization/content/organization.py
# Compiled at: 2011-06-07 12:12:00
from zope.interface import implements
from Products.CMFCore import permissions
try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.Organization import config
from Products.Organization.interfaces import IOrganization
from Products.Organization import OrganizationMessageFactory as _
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.document import finalizeATCTSchema
OrganizationSchema = ATDocument.schema.copy() + atapi.Schema(())
finalizeATCTSchema(OrganizationSchema)

class Organization(atapi.OrderedBaseFolder, ATDocument):
    """An Archetype for an Organization application"""
    implements(IOrganization)
    OrganizationSchema['title'].widget.label = 'Name'
    portal_type = meta_type = 'Organization'
    schema = OrganizationSchema
    _at_rename_after_creation = True

    def canSetDefaultPage(self):
        return False


atapi.registerType(Organization, config.PROJECTNAME)