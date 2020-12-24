# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mediawiki/Extensions/install.py
# Compiled at: 2008-10-06 10:31:13
"""Install the product
"""
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from iccommunity.mediawiki import GLOBALS
from iccommunity.mediawiki.config import DEPENDENCIES
import transaction

def install_dependencies(context):
    """Install dependencies"""
    quickinstaller = getToolByName(context, 'portal_quickinstaller')
    for product in DEPENDENCIES:
        if quickinstaller.isProductInstalled(product):
            quickinstaller.reinstallProducts([product])
            transaction.savepoint()
        else:
            quickinstaller.installProduct(product)
            transaction.savepoint()


def install(self):
    """External module to install the product.

    @type self: PloneSite
    @param self: The Plone site object

    @rtype: StringIO
    @return: Messages from the install process
    """
    out = StringIO()
    install_dependencies(self)
    setup_tool = getToolByName(self, 'portal_setup')
    if shasattr(setup_tool, 'runAllImportStepsFromProfile'):
        setup_tool.runAllImportStepsFromProfile('profile-iccommunity.mediawiki:default')
    else:
        old_context = setup_tool.getImportContextID()
        setup_tool.setImportContext('profile-iccommunity.mediawiki:default')
        setup_tool.runAllImportSteps()
        setup_tool.setImportContext(old_context)
    return out.getvalue()


def uninstall(self):
    """Uninstall method.
    """
    out = StringIO()
    print >> out, 'Uninstalling'
    return out.getvalue()