# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/autodelete/Extensions/Install.py
# Compiled at: 2008-03-07 05:43:03
import transaction
from Products.CMFCore.utils import getToolByName
PRODUCT_DEPENDENCIES = ('PloneMaintenance', )
EXTENSION_PROFILES = ('redomino.autodelete:default', )

def install(self, reinstall=False):
    portal_quickinstaller = getToolByName(self, 'portal_quickinstaller')
    portal_setup = getToolByName(self, 'portal_setup')
    for product in PRODUCT_DEPENDENCIES:
        if reinstall and portal_quickinstaller.isProductInstalled(product):
            if portal_quickinstaller.isProductInstallable(product):
                portal_quickinstaller.reinstallProducts([product])
                transaction.savepoint()
        elif not portal_quickinstaller.isProductInstalled(product):
            if portal_quickinstaller.isProductInstallable(product):
                portal_quickinstaller.installProduct(product)
                transaction.savepoint()

    for extension_id in EXTENSION_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        product_name = extension_id.split(':')[0]
        portal_quickinstaller.notifyInstalled(product_name)
        transaction.savepoint()