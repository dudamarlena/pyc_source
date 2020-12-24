# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/eCards/Extensions/Install.py
# Compiled at: 2008-11-11 20:26:18
from Products.eCards.config import PROJECTNAME, ALLTYPES, ALLSKINS, SendECard
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

def uninstall(self):
    out = StringIO()
    portal_factory = getToolByName(self, 'portal_factory')
    propsTool = getToolByName(self, 'portal_properties')
    siteProperties = getattr(propsTool, 'site_properties')
    navtreeProperties = getattr(propsTool, 'navtree_properties')
    types_tool = getToolByName(self, 'portal_types')
    factory_types = portal_factory.getFactoryTypes().keys()
    for t in ALLTYPES:
        if t in factory_types:
            factory_types.remove(t)

    portal_factory.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)
    print >> out, 'Removed eCards types from portal_factory tool'
    typesNotListed = list(navtreeProperties.getProperty('metaTypesNotToList'))
    for f in ALLTYPES:
        if f in typesNotListed:
            typesNotListed.remove(f)

    navtreeProperties.manage_changeProperties(metaTypesNotToList=typesNotListed)
    print >> out, 'Removed eCards types from metaTypesNotToList'
    typesUseViewAction = list(siteProperties.getProperty('typesUseViewActionInListings'))
    for f in ('eCard', ):
        if f in typesUseViewAction:
            typesUseViewAction.remove(f)

    siteProperties.manage_changeProperties(typesUseViewActionInListings=typesUseViewAction)
    print >> out, 'Removed eCard from typesUseViewActionInListings'
    skinstool = getToolByName(self, 'portal_skins')
    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName)
        path = [ i.strip() for i in path.split(',') ]
        for specific_layer in ALLSKINS:
            if specific_layer in path:
                path.remove(specific_layer)

        path = (',').join(path)
        skinstool.addSkinSelection(skinName, path)

    print >> out, 'Removed skin layers from all skin selections'
    workflow_tool = getToolByName(self, 'portal_workflow')
    del workflow_tool._chains_by_type['eCardCollection']
    print >> out, 'Removed the associated eCardCollection type chains'
    print >> out, '\nSuccessfully uninstalled %s.' % PROJECTNAME
    return out.getvalue()