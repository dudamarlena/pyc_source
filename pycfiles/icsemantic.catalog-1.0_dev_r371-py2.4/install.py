# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/catalog/Extensions/install.py
# Compiled at: 2008-10-06 10:31:12
"""Install the product.
"""
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from Products.Archetypes.Extensions.utils import install_subskin
from icsemantic.catalog import GLOBALS

def install(self):
    """External module to install the product.

    @type self: PloneSite
    @param self: The Plone site object

    @rtype: StringIO
    @return: Messages from the install process
    """
    out = StringIO()
    install_subskin(self, out, GLOBALS)
    setup_tool = getToolByName(self, 'portal_setup')
    if shasattr(setup_tool, 'runAllImportStepsFromProfile'):
        setup_tool.runAllImportStepsFromProfile('profile-icsemantic.catalog:default')
    else:
        old_context = setup_tool.getImportContextID()
        setup_tool.setImportContext('profile-icsemantic.catalog:default')
        setup_tool.runAllImportSteps()
        setup_tool.setImportContext(old_context)
    return out.getvalue()


def uninstall(self):
    """Uninstall method.
    """
    out = StringIO()
    print >> out, 'Uninstalling'
    return out.getvalue()