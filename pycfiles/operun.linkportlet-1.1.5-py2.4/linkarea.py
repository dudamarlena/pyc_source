# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/operun/linkportlet/content/linkarea.py
# Compiled at: 2009-11-23 18:17:49
"""A folder for links and link folders"""
from zope.interface import implements
from AccessControl import ClassSecurityInfo, getSecurityManager
from Products.CMFCore.permissions import View, ModifyPortalContent
from zope.component import getMultiAdapter
from Products.Archetypes.public import *
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
try:
    from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
except ImportError:
    from plone.app.folder.folder import ATFolder, ATFolderSchema

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from operun.linkportlet.interfaces import IOperunLinkArea, IOperunUnique
from operun.linkportlet.config import PROJECTNAME
from operun.linkportlet import OperunLinkPortletMessageFactory as _
OperunLinkAreaSchema = ATFolderSchema.copy()
OperunLinkAreaSchema['title'].storage = atapi.AnnotationStorage()
OperunLinkAreaSchema['title'].widget.label = _('title')
OperunLinkAreaSchema['title'].widget.description = _('title_desc', default='The title of this link area')
OperunLinkAreaSchema['description'].widget.visible = False
defaults_dict = {'excludeFromNav': True, 'allowDiscussion': False, 'nextPreviousEnabled': False}
for propertyField in ('excludeFromNav', 'allowDiscussion', 'nextPreviousEnabled'):
    OperunLinkAreaSchema[propertyField].default = defaults_dict[propertyField]
    OperunLinkAreaSchema[propertyField].widget.visible = False
    OperunLinkAreaSchema[propertyField].languageIndependent = 1

finalizeATCTSchema(OperunLinkAreaSchema, folderish=True, moveDiscussion=False)
for propertyField in ('excludeFromNav', 'allowDiscussion', 'nextPreviousEnabled'):
    OperunLinkAreaSchema.changeSchemataForField(propertyField, 'default')

class OperunLinkArea(ATFolder):
    """A folder which contains links and link folders.
    """
    __module__ = __name__
    implements(IOperunLinkArea, IOperunUnique)
    portal_type = 'operun Link Area'
    _at_rename_after_creation = True
    schema = OperunLinkAreaSchema
    title = atapi.ATFieldProperty('title')
    security = ClassSecurityInfo()
    security.declareProtected(View, 'index_html')

    def index_html(self, REQUEST=None, RESPONSE=None):
        """Download the file
        """
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self):
            self.REQUEST.RESPONSE.redirect('%s/view' % ('/').join(self.getPhysicalPath()))
        else:
            portal_state = getMultiAdapter((self, REQUEST), name='plone_portal_state')
            RESPONSE.redirect(portal_state.portal_url())
            return ''
        return ''


atapi.registerType(OperunLinkArea, PROJECTNAME)