# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icnews/acquire/Extensions/install.py
# Compiled at: 2008-10-06 10:31:17
"""
@author: Juan Pablo Gimenez
@contact: jpg@rcom.com.ar
"""
__author__ = 'Juan Pablo Gimenez <jpg@rcom.com.ar>'
__docformat__ = 'plaintext'
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from icnews.acquire.config import *

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
        >>> from icnews.acquire.config import *
        >>> qi = portal.portal_quickinstaller
        >>> installed = [ prod['id'] for prod in qi.listInstalledProducts() ]
        >>> for dependency in DEPENDENCIES:
        ...     dependency in installed

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
        >>> from icnews.acquire.config import *
        >>> psetup = self.portal.portal_setup

    just test we have registered the profile...
        >>> profilename = PROJECTNAME + ':default'
        >>> PACKAGENAME in [profile['product'] for profile in psetup.listProfileInfo()]
        True
        >>> profilename in [profile['id'] for profile in psetup.listProfileInfo()]
        True

    now we can test some stuff modified by that template...
        >>> None # Nada todavia...

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
        >>> from icnews.acquire.config import *
        >>> qi = self.portal.portal_quickinstaller
        >>> installed = [ prod['id'] for prod in qi.listInstalledProducts() ]
        >>> PACKAGENAME in installed
        True

    """
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    print >> out, 'Installing Dependencies'
    res = install_dependencies(portal, out)
    print >> out, res or 'no output'
    print >> out, 'Import GS Profiles'
    res = import_gs_profiles(portal, out)
    print >> out, res or 'no output'
    return out.getvalue()


def uninstall(self):
    """
    External module to uninstall the product...
        @type self: PloneSite
        @param self: The Plone site object

        @rtype: StringIO
        @return: Messages from the install process

    some tests here...
        >>> from icnews.acquire.config import *
        >>> qi = self.portal.portal_quickinstaller
        >>> installed = [ prod['id'] for prod in qi.listInstalledProducts() ]
        >>> PACKAGENAME in installed
        True

        >>> qi.uninstallProducts((PACKAGENAME,))
        >>> installed = [ prod['id'] for prod in qi.listInstalledProducts() ]
        >>> PACKAGENAME in installed
        False

    """
    out = StringIO()
    print >> out, 'Uninstalling'
    return out.getvalue()