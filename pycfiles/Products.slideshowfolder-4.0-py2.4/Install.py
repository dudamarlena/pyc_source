# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/Extensions/Install.py
# Compiled at: 2008-06-02 02:45:55
from Products.slideshowfolder.config import *
from Products.CMFCore.utils import getToolByName
from Products.slideshowfolder.Extensions.utils import restoreAllFolders
from Products.slideshowfolder.Extensions.utils import removeAction
from Products.slideshowfolder import HAS_PLONE30

def install(portal):
    """Our install process is to import our Generic Setup profile and,
    if on Plone 2.5, install CMFonFive."""
    if not HAS_PLONE30:
        qit = getToolByName(portal, 'portal_quickinstaller')
        products_to_install = ['CMFonFive']
        installable_products = [ x['id'] for x in qit.listInstallableProducts(skipInstalled=1) ]
        installed_products = [ x['id'] for x in qit.listInstalledProducts() ]
        for product in products_to_install:
            if product in installable_products:
                qit.installProduct(product)
            elif product not in installed_products:
                raise RuntimeError('Dependent product %s not available to install' % product)

    setup_tool = getToolByName(portal, 'portal_setup')
    if not HAS_PLONE30:
        original_context = setup_tool.getImportContextID()
        setup_tool.setImportContext('profile-slideshowfolder:default')
        feedback = setup_tool.runAllImportSteps()
        setup_tool.setImportContext(original_context)
    else:
        feedback = {}
        feedback.update(setup_tool.runAllImportStepsFromProfile('profile-slideshowfolder:default'))
        feedback.update(setup_tool.runAllImportStepsFromProfile('profile-slideshowfolder:plone3'))
    feedback = feedback['messages']
    gs_output = [ '%s: %s' % (k, feedback[k]) for k in feedback.keys() if feedback[k] ]
    return 'Ran Slideshow Folder import steps.: \n    %s' % ('\n').join(gs_output)


def uninstall(portal, reinstall=False):
    """CSS, js, and skin registration are all automatically undone for us.
        We just need to remove our skin layers and actions.
        
        We also do a relatively expensive traversal of all folders and "unmake" them
        if they are slideshow folders.  If we're not reinstalling, that is.
    """
    feedback = ''
    skinstool = getToolByName(portal, 'portal_skins')
    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName)
        path = [ i.strip() for i in path.split(',') ]
        prev = len(path)
        for old_skin in ('slideshowfolder', 'slideshowjavascript'):
            if old_skin in path:
                path.remove(old_skin)

        if prev != len(path):
            path = (',').join(path)
            skinstool.addSkinSelection(skinName, path)

    feedback += 'Removed slideshow skin layers\n'
    portal_actions = getToolByName(portal, 'portal_actions')
    actions_to_remove = ('unmakeSlideshow', 'makeSlideshow', 'slideshow_settings')
    for action in actions_to_remove:
        removeAction(action, portal_actions)

    feedback += 'Removed extraneous actions from portal_actions\n'
    if not reinstall:
        feedback += restoreAllFolders(portal)
    return feedback