# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/thesaurus/Extensions/install.py
# Compiled at: 2008-10-06 10:31:07
"""
$Id: install.py 358 2008-07-29 18:56:21Z flarumbe $
"""
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from Products.Archetypes.Extensions.utils import install_subskin
from icsemantic.thesaurus.config import *
from icsemantic.thesaurus.interfaces import IThesaurus
from icsemantic.thesaurus.Thesaurus import Thesaurus

def install_configlets(out):
    """
    Method to install platecom user properties...
        @type: portal: PloneSite
        @type out: StringIO

        @rtype: StringIO
        @return: Messages from the GS process
    """
    configTool = getToolByName(portal(self), 'portal_controlpanel', None)
    if configTool:
        for conf in CONFIGLETS:
            configTool.registerConfiglet(**conf)
            out.write('Added configlet %s\n' % conf['id'])

    return out


def install_dependencies(self):
    """
    Test if everything at DEPENDENCIES gets installed...
        >>> 1
        1
    """
    out = StringIO()
    quickinstaller = portal(self).portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, 'Installing dependency %s:' % dependency
        quickinstaller.installProduct(dependency)

    return out


def install(self):
    """
    External module to install the product...
        @type self: PloneSite
        @param self: The Plone site object

        @rtype: StringIO
        @return: Messages from the install process

    some tests here...
        >>> from icsemantic.thesaurus.config import *
        >>> qi = self.portal.portal_quickinstaller
        >>> installed = [ prod['id'] for prod in qi.listInstalledProducts() ]
        >>> PACKAGENAME in installed
        True

    """
    out = StringIO()
    print >> out, 'Installing Dependencies'
    install_dependencies(self)
    setup_tool = getToolByName(self, 'portal_setup')
    if shasattr(setup_tool, 'runAllImportStepsFromProfile'):
        pass
    install_thesaurus_utility(self, out)
    install_subskin(self, out, GLOBALS)
    res = import_gs_profiles(self, out)
    return out.getvalue()


def install_thesaurus_utility(self, out):
    portal = getToolByName(self, 'portal_url').getPortalObject()
    sm = portal.getSiteManager()
    if not sm.queryUtility(IThesaurus, name=''):
        try:
            sm.registerUtility(Thesaurus(), IThesaurus, '')
        except:
            sm.registerUtility(IThesaurus, Thesaurus(), '')

    out.write('Adding Thesaurus Utility\n')


def addDocument(portal, document_id, document_title, keywords):
    portal.invokeFactory('Document', document_id)
    doc = portal[document_id]
    doc.setTitle(document_title)
    doc.setSubject(keywords)
    return doc


def deleteDocument(portal, document_id):
    portal.manage_delObjects(document_id)


def import_gs_profiles(self, out):
    """
    Method to install GS profiles...
        @type out: StringIO
        @param out: The object to append the output

        @rtype: StringIO
        @return: Messages from the GS process

    some tests here...
        >>> from icsemantic.core.config import *
        >>> psetup = self.portal.portal_setup

    just test we have registered the profile...
        >>> profilename = PROJECTNAME + ':default'
        >>> PACKAGENAME in [profile['product'] for profile in psetup.listProfileInfo()]
        True
        >>> profilename in [profile['id'] for profile in psetup.listProfileInfo()]
        True

    now we can test some stuff modified but that template...
        >>> 'icSemantic' in [ai.getTitle() for ai in portal.portal_actionicons.listActionIcons()]
        True

    No se porque este no anda, anda bien en el test funcional...
        >>> # [ai['name'] for ai in portal.portal_controlpanel.listActionInfos()] True

    """
    print >> out, 'Import GS Profiles'
    setup_tool = getToolByName(portal(self), 'portal_setup')
    profile_name = 'profile-' + PROJECTNAME + ':default'
    if shasattr(setup_tool, 'runAllImportStepsFromProfile'):
        print >> out, setup_tool.runAllImportStepsFromProfile(profile_name)
    else:
        old_context = setup_tool.getImportContextID()
        print >> out, setup_tool.setImportContext(profile_name)
        print >> out, setup_tool.runAllImportSteps()
        print >> out, setup_tool.setImportContext(old_context)
    return out


def uninstall(self):
    """
    Test if everything gets installed...
        >>> 1
        1
    """
    out = StringIO()
    print >> out, 'Uninstalling'
    return out.getvalue()


def portal(self):
    return getToolByName(self, 'portal_url').getPortalObject()