# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/Extensions/Install.py
# Compiled at: 2010-03-10 13:47:45
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.UpfrontContacts.person_schema import person_schema
from Products.UpfrontContacts.Organisation import schema as organisation_schema
from Products.UpfrontContacts.UpfrontContactsTool import UpfrontContactsTool
from Products.UpfrontContacts.config import PROJECTNAME, GLOBALS, COUNTRY_NAMES
from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.utils import generateCategorySetIdForType
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from StringIO import StringIO

def install(self):
    out = StringIO()
    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    install_subskin(self, out, GLOBALS)
    install_dependencies(self, out)
    install_tools(self, out)
    setup_properties(self, out)
    setup_membrane(self, out)
    setup_portal_factory(self, out)
    setup_catalog(self, out)
    if self.portal_actionicons.queryActionInfo('plone', 'vcard') is None:
        self.portal_actionicons.addActionIcon('plone', 'vcard', 'vcard.png', title='vCard')
    mdc = self.portal_types['MemberDataContainer']
    mdc.allowed_content_types = mdc.allowed_content_types + ('Person', )
    wft = getToolByName(self, 'portal_workflow')
    wft.setChainForPortalTypes(['Person'], 'member_approval_workflow')
    out.write('Successfully installed %s.' % PROJECTNAME)
    return out.getvalue()


def install_tools(portal, out):
    if not hasattr(portal, 'upfront_contacts_tool'):
        portal.manage_addProduct[PROJECTNAME].manage_addTool(UpfrontContactsTool.meta_type, None)
        print >> out, 'Successfully installed Upfront Contacts Tool.'
    return


def install_dependencies(portal, out, required=1):
    qi = getToolByName(portal, 'portal_quickinstaller', None)
    if qi is None and required:
        raise RuntimeError, "portal_quickinstaller tool could not be found, and it is required to install UpfrontContacts' dependencies"
    if not qi.isProductInstalled('ATExtensions'):
        qi.installProduct('ATExtensions')
        print >> out, 'Installing ATExtensions'
    return


def setup_properties(portal, out):
    ptool = getToolByName(portal, 'portal_properties')
    ps = getattr(ptool, 'upfrontcontacts_properties', None)
    if not ps:
        ptool.addPropertySheet('upfrontcontacts_properties', 'UpfrontContacts Properties')
        ps = getattr(ptool, 'upfrontcontacts_properties')
        ps._properties = ps._properties + ({'id': 'country_names', 'type': 'lines', 'mode': 'w'},)
        ps._updateProperty('country_names', COUNTRY_NAMES)
        out.write('Added %s properties.' % PROJECTNAME)
    else:
        out.write('%s properties already installed.' % PROJECTNAME)
    return


def setup_membrane(portal, out):
    portal.membrane_tool.registerMembraneType('Person')
    print >> out, 'Registered Person as membrane type'
    cat_map = ICategoryMapper(portal.membrane_tool)
    person_states = ['pending', 'private', 'public']
    cat_set = generateCategorySetIdForType('Person')
    if not cat_map.hasCategorySet(cat_set):
        cat_map.addCategorySet(cat_set)
        cat_map.addCategory(cat_set, ACTIVE_STATUS_CATEGORY)
        for state in person_states:
            cat_map.addToCategory(cat_set, ACTIVE_STATUS_CATEGORY, state)

    else:
        cat_map.replaceCategoryValues(cat_set, ACTIVE_STATUS_CATEGORY, person_states)
    print >> out, 'Set membrane_tool status_map states for Person'


def setup_portal_factory(portal, out):
    factory = getToolByName(portal, 'portal_factory', None)
    if factory is not None:
        types = factory.getFactoryTypes().keys()
        for metaType in ('Person', 'Organisation'):
            if metaType not in types:
                types.append(metaType)

        factory.manage_setPortalFactoryTypes(listOfTypeIds=types)
        print >> out, 'Added content types to portal_factory.'
    return


def setup_catalog(portal, out):
    if 'UID' not in portal.portal_catalog.schema():
        portal.portal_catalog.addColumn('UID')