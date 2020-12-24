# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/core/Extensions/install.py
# Compiled at: 2008-10-06 10:31:14
"""
Metodos de install para iccommunity.core

@author: Juan Pablo Gimenez
@contact: jpg@rcom.com.ar
"""
__author__ = 'Juan Pablo Gimenez <jpg@rcom.com.ar>'
__docformat__ = 'plaintext'
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from Products.Archetypes.Extensions.utils import install_subskin
from iccommunity.core.config import *

def install_configlets(portal, out):
    """
    Method to install platecom user properties...
        @type: portal: PloneSite
        @type out: StringIO

        @rtype: StringIO
        @return: Messages from the GS process
    """
    configTool = getToolByName(portal, 'portal_controlpanel', None)
    if configTool:
        for conf in CONFIGLETS:
            configTool.registerConfiglet(**conf)
            out.write('Added configlet %s\n' % conf['id'])

    return out


def uninstall_configlets(portal, out):
    """
    Method to uninstall platecom user properties...
        @type: portal: PloneSite
        @type out: StringIO

        @rtype: StringIO
        @return: Messages from the GS process
    """
    configTool = getToolByName(portal, 'portal_controlpanel')
    if configTool:
        for conf in CONFIGLETS:
            configTool.unregisterConfiglet(conf['id'])
            out.write('Removed configlet %s\n' % conf['id'])

    return out


def install_dependencies(portal, out):
    """
    Method to install dependencies...
        @type portal: PloneSite
        @param portal: The Plone site object
        @type out: StringIO
        @param out: The object to append the output

        @rtype: StringIO
        @return: Messages from the GS process

    some tests here...

    """
    quickinstaller = portal.portal_quickinstaller
    for dependency in DEPENDENCIES:
        print >> out, 'Installing dependency %s:' % dependency
        quickinstaller.installProduct(dependency)

    return out


def import_gs_profiles(portal, out):
    """
    Method to install GS profiles...
        @type portal: PloneSite
        @param portal: The Plone site object
        @type out: StringIO
        @param out: The object to append the output

        @rtype: StringIO
        @return: Messages from the GS process

    some tests here...
        >>> from iccommunity.core.config import *
        >>> psetup = self.portal.portal_setup

    just test we have registered the profile...
        >>> profilename = PROJECTNAME + ':default'
        >>> PACKAGENAME in [profile['product'] for profile in psetup.listProfileInfo()]
        True
        >>> profilename in [profile['id'] for profile in psetup.listProfileInfo()]
        True

    now we can test some stuff modified but that template...
        >>> 'icCommunity' in [ai.getTitle() for ai in portal.portal_actionicons.listActionIcons()]
        True

    No se porque este no anda, anda bien en el test funcional...
        >>> # [ai['name'] for ai in portal.portal_controlpanel.listActionInfos()] True

    """
    setup_tool = getToolByName(portal, 'portal_setup')
    profile_name = 'profile-' + PROJECTNAME + ':default'
    if shasattr(setup_tool, 'runAllImportStepsFromProfile'):
        print >> out, setup_tool.runAllImportStepsFromProfile(profile_name)
    else:
        old_context = setup_tool.getImportContextID()
        print >> out, setup_tool.setImportContext(profile_name)
        print >> out, setup_tool.runAllImportSteps()
        print >> out, setup_tool.setImportContext(old_context)
    return out


def install(self):
    """
    External module to install the product...
        @type self: PloneSite
        @param self: The Plone site object

        @rtype: StringIO
        @return: Messages from the install process

    some tests here...
        >>> from iccommunity.core.config import *
        >>> qi = self.portal.portal_quickinstaller
        >>> installed = [ prod['id'] for prod in qi.listInstalledProducts() ]
        >>> PACKAGENAME in installed
        True

    """
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    install_subskin(self, out, GLOBALS)
    print >> out, 'Installing Dependencies'
    res = install_dependencies(portal, out)
    print >> out, res or 'no output'
    print >> out, 'Installing Configlets'
    res = install_configlets(portal, out)
    print >> out, res or 'no output'
    print >> out, 'Import GS Profiles'
    res = import_gs_profiles(portal, out)
    print >> out, res or 'no output'
    return out.getvalue()


def unimport_gs_profiles(portal, out):
    """
    Method to uninstall GS profiles...
        @type portal: PloneSite
        @param portal: The Plone site object
        @type out: StringIO
        @param out: The object to append the output

        @rtype: StringIO
        @return: Messages from the GS process

    some tests here...
        >>> from iccommunity.core.config import *
        >>> psetup = self.portal.portal_setup

    just test we have registered the profile...
        >>> profilename = PROJECTNAME + ':default'
        >>> PACKAGENAME in [profile['product'] for profile in psetup.listProfileInfo()]
        True
        >>> profilename in [profile['id'] for profile in psetup.listProfileInfo()]
        True

    now we can test some stuff modified but that template...

    """
    setup_tool = getToolByName(portal, 'portal_setup')
    profile_name = 'profile-' + PROJECTNAME + ':uninstall'
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
    External module to uninstall the product...
        @type self: PloneSite
        @param self: The Plone site object

        @rtype: StringIO
        @return: Messages from the install process

    some tests here...
        >>> from iccommunity.core.config import *
        >>> qi = self.portal.portal_quickinstaller
        >>> installed = [ prod['id'] for prod in qi.listInstalledProducts() ]
        >>> PACKAGENAME in installed
        True

        >>> self.setRoles(['Manager',])
        >>> qi.uninstallProducts((PACKAGENAME,))
        >>> installed = [ prod['id'] for prod in qi.listInstalledProducts() ]
        >>> PACKAGENAME in installed
        False

    """
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    print >> out, 'Uninstalling'
    print >> out, 'Uninstalling Configlets'
    res = uninstall_configlets(portal, out)
    print >> out, res or 'no output'
    print >> out, 'UnImport GS Profiles'
    res = unimport_gs_profiles(portal, out)
    print >> out, res or 'no output'
    return out.getvalue()