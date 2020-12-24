# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/CSSManager/Extensions/Install.py
# Compiled at: 2008-09-18 15:18:08
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CSSManager.config import *
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

def install(self):
    out = StringIO()
    self.manage_addProduct['CSSManager'].manage_addTool(type='css_tool')
    try:
        from Products.CSSManager.config import DEPENDENCIES
    except:
        DEPENDENCIES = []

    portal = getToolByName(self, 'portal_url').getPortalObject()
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, 'Installing dependency %s:' % dependency
        quickinstaller.installProduct(dependency)
        get_transaction().commit(1)

    install_subskin(self, out, GLOBALS)
    portal = getToolByName(self, 'portal_url').getPortalObject()
    portal.portal_controlpanel.registerConfiglet(**cssmanager_configlet)
    print >> out, 'Successfully installed %s.' % PROJECTNAME
    return out.getvalue()


def _skinsTool(self):
    return getToolByName(self, 'portal_skins')


def uninstall(self):
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    try:
        self.portal_controlpanel.unregisterApplication(PROJECTNAME)
    except:
        pass

    print >> out, 'Removing layers from portal_skins...'
    deleteLayers(_skinsTool(self), ['CSSManager'])
    return out.getvalue()


def deleteLayers(skinsTool, layersToDelete):
    """Remove each of the layers in `layersToDelete` from all skins.
    
    (We check them all, in case the user manually inserted it into some.)
    
    Pass getToolByName(portal, 'portal_skins') for `skinsTool`.
    
    """
    for skinName in skinsTool.getSkinSelections():
        layers = [ x.strip() for x in skinsTool.getSkinPath(skinName).split(',') ]
        try:
            for curLayer in layersToDelete:
                layers.remove(curLayer)

        except ValueError:
            pass

        skinsTool.addSkinSelection(skinName, (',').join(layers))