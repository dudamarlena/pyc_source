# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\Extensions\Install.py
# Compiled at: 2009-03-02 16:14:23
from cStringIO import StringIO
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes import listTypes
from Products.Archetypes.Extensions.utils import installTypes
from Products.CMFCore.utils import getToolByName
from Products.FlashVideo.config import *
from Products.FlashVideo.utils import IS_PLONE_30
from Products.FlashVideo.utils import IS_PLONE_31

def install(self):
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    portal_setup = getToolByName(portal, 'portal_setup', None)
    if portal_setup:
        print >> out, 'Installation using Generic Setup'
        if hasattr(portal_setup, 'runAllImportStepsFromProfile'):
            portal_setup.runAllImportStepsFromProfile('profile-FlashVideo:default')
        else:
            old_context = portal_setup.getImportContextID()
            portal_setup.setImportContext('profile-FlashVideo:default')
            portal_setup.runAllImportSteps()
            portal_setup.setImportContext(old_context)
    else:
        print >> out, 'Ordinary installation'
        installFSS(portal, out)
        installPloneTypes(portal, out, PROJECTNAME)
        install_subskin(portal, out, GLOBALS)
        hideTypesInNavigation(portal, out)
        addViewActions(portal, out)
        registerMimeType(portal, out)
        registerContentType(portal, out)
    print >> out, 'Installation completed.'
    return out.getvalue()


def installPloneTypes(portal, out, projectname):
    """
    Register Archetype content types
    """
    typeInfo = listTypes(projectname)
    installTypes(portal, out, typeInfo, projectname)
    print >> out, 'Types registered'


def addViewActions(portal, out):
    """
    """
    portal_properties = getToolByName(portal, 'portal_properties')
    site_properties = portal_properties.site_properties
    actions = list(site_properties.getProperty('typesUseViewActionInListings', ()))
    for t in (FLASHVIDEO_PORTALTYPE,):
        if t not in actions:
            actions.append(t)

    site_properties.typesUseViewActionInListings = tuple(actions)
    print >> out, 'View actions in listings updated'


def installFSS(portal, out=None):
    """
    Install FileSystemStorage if exists
    """
    if not out:
        portal = portal.getSite()
        out = StringIO()
    root = portal.getPhysicalRoot()
    Products = root.Control_Panel.Products
    portal_quickinstaller = getToolByName(portal, 'portal_quickinstaller', None)
    if 'FileSystemStorage' in Products.objectIds():
        if portal_quickinstaller.isProductInstallable('FileSystemStorage'):
            if not portal_quickinstaller.isProductInstalled('FileSystemStorage'):
                portal_quickinstaller.installProduct('FileSystemStorage')
                print >> out, 'Installing FileSystemStorage'
            else:
                print >> out, 'FileSystemStorage already installed.'
        else:
            print >> out, 'FileSystemStorage not installable.'
    else:
        print >> out, 'FileSystemStorage Product not added.'
    return


def hideTypesInNavigation(portal, out):
    """
    Hide selected types from the navtree
    """
    portal_properties = getToolByName(portal, 'portal_properties', None)
    navtree_properties = portal_properties.navtree_properties
    hidden_list = (FLASHVIDEO_PORTALTYPE,)
    types_not_to_list = list(navtree_properties.getProperty('metaTypesNotToList', ()))
    for t in hidden_list:
        if t not in types_not_to_list:
            types_not_to_list.append(t)

    navtree_properties._setPropValue('metaTypesNotToList', types_not_to_list)
    print >> out, 'Types hidden from navigation: %s' % (', ').join(hidden_list)
    return


def removeDuplicateActionsInTypes(portal, out=None):
    """
    In Plone 3 xml configuraton adds duplicated 'local_roles' action.
    Remove it
    """
    if not out:
        portal = portal.getSite()
        out = StringIO()
    if IS_PLONE_30 or IS_PLONE_31:
        portal_types = getToolByName(portal, 'portal_types', None)
        for portal_type in (FLASHVIDEO_PORTALTYPE, FLASHVIDEOFOLDER_PORTALTYPE, FLASHVIDEOPLAYLIST_PORTALTYPE):
            p_type = portal_types.getTypeInfo(portal_type)
            type_actions = p_type._actions
            actions_ids = [ x.getId() for x in type_actions ]
            for i in range(len(type_actions)):
                action = type_actions[i]
                expr = action.getActionExpression()
                if hasattr(expr, 'text'):
                    expr = expr.text
                if action.getId() == 'local_roles' and expr == 'string:${object_url}/sharing':
                    p_type.deleteActions(selections=(actions_ids.index('local_roles'),))
                    print >> out, "Duplicate 'local_roles' action from '%s' deleted" % portal_type
                    break

    return


def registerMimeType(portal, out=None):
    """
    Adds information to mimetypes_registry
    """
    if not out:
        portal = portal.getSite()
        out = StringIO()
    info = {'id': 'Flash Video', 'mimetypes': ['video/x-flv'], 'extensions': ['flv'], 'icon_path': 'flashvideo_icon.gif', 'binary': True, 'globs': ['*.flv']}
    mimetypes_registry = getToolByName(portal, 'mimetypes_registry')
    if not mimetypes_registry.lookup(info['mimetypes']):
        mimetypes_registry.manage_addMimeType(**info)
        print >> out, "MIME type '%s' added to register" % info['id']
    else:
        print >> out, "MIME type '%s' already in register" % info['id']


def registerContentType(portal, out=None):
    """
    Adds information to content_type_registry
    """
    if not out:
        portal = portal.getSite()
        out = StringIO()
    infos = [{'id': 'flv', 'type': 'extension', 'extensions': 'flv', 'portal_type': 'Flash Video'}, {'id': 'video/x-flv', 'type': 'major_minor', 'major': 'video', 'minor': 'x-flv', 'portal_type': 'Flash Video'}]
    content_type_registry = getToolByName(portal, 'content_type_registry')
    predicate_ids = content_type_registry.predicate_ids
    for info in infos:
        if info['id'] not in predicate_ids:
            content_type_registry.addPredicate(info['id'], info['type'])
            predicate = content_type_registry.getPredicate(info['id'])
            if info['type'] == 'extension':
                predicate.edit(info['extensions'])
            elif info['type'] == 'major_minor':
                predicate.edit(info['major'], info['minor'])
            content_type_registry.assignTypeName(info['id'], info['portal_type'])
            print >> out, "Predicate '%s': '%s' for '%s' added to register" % (info['id'], info['type'], info['portal_type'])
        else:
            print >> out, "Predicate '%s': '%s' for '%s' already exists in register" % (info['id'], info['type'], info['portal_type'])

    content_type_registry.reorderPredicate('video', len(content_type_registry.listPredicates()) - 1)
    print >> out, "Predicate 'video' moved to bottom of register"