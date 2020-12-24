# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icnews/core/Extensions/install.py
# Compiled at: 2008-10-06 10:31:17
"""Installation
"""
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from Products.Archetypes.Extensions.utils import install_subskin
from icnews.core.config import *

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
        >>> from icnews.core.config import *
        >>> psetup = self.portal.portal_setup

    just test we have registered the profile...
        >>> profilename = PROJECTNAME + ':default'
        >>> PACKAGENAME in [profile['product'] for profile in psetup.listProfileInfo()]
        True
        >>> profilename in [profile['id'] for profile in psetup.listProfileInfo()]
        True

    now we can test some stuff modified but that template...
        >>> 'icNews' in [ai.getTitle() for ai in portal.portal_actionicons.listActionIcons()]
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
    """
    out = StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    install_subskin(self, out, GLOBALS)
    print >> out, 'Installing Dependencies'
    res = install_dependencies(portal, out)
    print >> out, res or 'no output'
    print >> out, 'Import GS Profiles'
    res = import_gs_profiles(portal, out)
    print >> out, res or 'no output'
    return out.getvalue()