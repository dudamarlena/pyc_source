# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/ploneformgen/readonlystringfield/Extensions/Install.py
# Compiled at: 2009-03-24 10:51:59
import transaction
from Products.CMFCore.utils import getToolByName
PRODUCT_DEPENDENCIES = ('PloneFormGen', )
EXTENSION_PROFILES = ('quintagroup.ploneformgen.readonlystringfield:default', )
UNINSTALL_PROFILES = ('quintagroup.ploneformgen.readonlystringfield:uninstall', )

def install(self, reinstall=False):
    """Install a set of products (which themselves may either use Install.py
    or GenericSetup extension profiles for their configuration) and then
    install a set of extension profiles.
    
    One of the extension profiles we install is that of this product. This
    works because an Install.py installation script (such as this one) takes
    precedence over extension profiles for the same product in 
    portal_quickinstaller. 
    
    We do this because it is not possible to install other products during
    the execution of an extension profile (i.e. we cannot do this during
    the importVarious step for this profile).
    """
    portal_quickinstaller = getToolByName(self, 'portal_quickinstaller')
    portal_setup = getToolByName(self, 'portal_setup')
    for product in PRODUCT_DEPENDENCIES:
        if reinstall:
            if portal_quickinstaller.isProductInstalled(product):
                portal_quickinstaller.reinstallProducts([product])
                transaction.savepoint()
            portal_quickinstaller.isProductInstalled(product) or portal_quickinstaller.installProduct(product)
            transaction.savepoint()

    for extension_id in EXTENSION_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        product_name = extension_id.split(':')[0]
        portal_quickinstaller.notifyInstalled(product_name)
        transaction.savepoint()


def uninstall(self):
    portal_setup = getToolByName(self, 'portal_setup')
    for extension_id in UNINSTALL_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        product_name = extension_id.split(':')[0]
        transaction.savepoint()