# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/semicinternet/theme/cambrils/Extensions/Install.py
# Compiled at: 2011-07-14 07:13:47
import transaction
from Products.CMFCore.utils import getToolByName
UNINSTALL_PROFILES = [
 'semicinternet.theme.cambrils:uninstall']

def uninstall(self):
    portal_setup = getToolByName(self, 'portal_setup')
    for extension_id in UNINSTALL_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id)
        product_name = extension_id.split(':')[0]
        transaction.savepoint()