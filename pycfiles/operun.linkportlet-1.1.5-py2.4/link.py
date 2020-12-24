# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/operun/linkportlet/content/link.py
# Compiled at: 2009-04-13 17:17:50
"""Definition of the Operun Link content type and associated schemata
and other logic.
"""
from zope.interface import implements
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.permissions import View, ModifyPortalContent
from AccessControl import ClassSecurityInfo, getSecurityManager
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.public import *

from Products.Archetypes import atapi
from Products.Archetypes.interfaces import IObjectPostValidation
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from operun.linkportlet.interfaces import IOperunLink
from operun.linkportlet.config import PROJECTNAME, LINK_TYPE_VOCABULARY, LINK_TARGET_VOCABULARY
from operun.linkportlet import OperunLinkPortletMessageFactory as _
OperunLinkSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((atapi.StringField('linkType', required=True, enforceVocabulary=True, vocabulary=LINK_TYPE_VOCABULARY, value='internal', languageIndependent=1, storage=atapi.AnnotationStorage(), widget=atapi.SelectionWidget(label=_('link_type', default='Link Type'), description=_('link_type_desc', default='Select whether this is an internal or external link.'))), atapi.ReferenceField('internalLink', relationship='internal_link', multiValued=False, required=False, languageIndependent=1, storage=atapi.AnnotationStorage(), widget=ReferenceBrowserWidget(label=_('internal_remoteURL', default='Internal Link'), description=_('internal_remoteURL_desc', default='A link to content inside the CMS.'), allow_browse=True)), atapi.StringField('externalLink', required=False, searchable=True, primary=False, validators=('isURL', ), languageIndependent=1, storage=atapi.AnnotationStorage(), widget=atapi.StringWidget(description=_('external_remoteURL_desc', default='A link to content outside of the CMS.'), label=_('external_remoteURL', default='External Link'))), atapi.StringField('linkTarget', required=True, enforceVocabulary=True, vocabulary=LINK_TARGET_VOCABULARY, default='same', languageIndependent=1, storage=atapi.AnnotationStorage(), widget=atapi.SelectionWidget(label=_('link_target', default='Target Window'), description=_('link_target_desc', default='Select whether the link should be opened in the same window or a new one.')))))
OperunLinkSchema['title'].storage = atapi.AnnotationStorage()
OperunLinkSchema['description'].storage = atapi.AnnotationStorage()
defaults_dict = {'excludeFromNav': True, 'allowDiscussion': False}
for propertyField in ('excludeFromNav', 'allowDiscussion'):
    OperunLinkSchema[propertyField].default = defaults_dict[propertyField]
    OperunLinkSchema[propertyField].widget.visible = False
    OperunLinkSchema[propertyField].languageIndependent = 1

finalizeATCTSchema(OperunLinkSchema, folderish=False, moveDiscussion=False)
for propertyField in ('excludeFromNav', 'allowDiscussion'):
    OperunLinkSchema.changeSchemataForField(propertyField, 'default')

class OperunLink(base.ATCTContent):
    """An internal link
    """
    __module__ = __name__
    implements(IOperunLink)
    portal_type = 'operun Link'
    _at_rename_after_creation = True
    schema = OperunLinkSchema
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    linkType = atapi.ATFieldProperty('linkType')
    internalLink = atapi.ATReferenceFieldProperty('internalLink')
    externalLink = atapi.ATFieldProperty('externalLink')
    linkTarget = atapi.ATFieldProperty('linkTarget')

    def getRemoteUrl(self):
        """Return the URL for the link
        """
        if self.getLinkType() == 'internal':
            internal_link = self.getInternalLink()
            return internal_link and internal_link.UID() or None
        else:
            return self.getExternalLink()
        return


atapi.registerType(OperunLink, PROJECTNAME)

class ValidateLink(object):
    """Validate whether some fields have been set if location based search has
       been selected.
    """
    __module__ = __name__
    implements(IObjectPostValidation)
    link_type_field = 'linkType'
    link_field_mapping = {'internal': 'internalLink', 'external': 'externalLink'}

    def __init__(self, context):
        self.context = context

    def __call__(self, request):
        link_type = self.context.getLinkType()
        link_field = self.link_field_mapping.get(link_type, None)
        err_dict = {}
        if link_field is None:
            return
        val = request.form.get(link_field, request.get(link_field, None))
        if val in (None, ''):
            err_dict[link_field] = _('selected_link_missing', default='Please enter an %s link.' % link_type)
        else:
            site = getSite()
            catalog = getToolByName(site, 'portal_catalog')
            uid = self.context.UID()
            url = ''
            if link_type == 'external':
                url = val.endswith('/') and val[:-1] or val
            link_targets = catalog(UID=val)
            if len(link_targets) == 1:
                url = link_targets[0].getObject().absolute_url()
        results = catalog(portal_type='operun Link')
        for brain in results:
            if brain.getRemoteUrl is not None:
                brain_url = brain.getRemoteUrl.endswith('/') and brain.getRemoteUrl[:-1] or brain.getRemoteUrl
                if brain_url == url and brain.UID != uid:
                    err_dict[link_field] = _('link_already_exists', default='This link has already been used somewhere else.')
                    break

        return err_dict and err_dict or None