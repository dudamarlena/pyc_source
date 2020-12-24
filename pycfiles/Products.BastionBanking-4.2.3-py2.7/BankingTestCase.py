# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/tests/BankingTestCase.py
# Compiled at: 2015-07-18 19:38:10
import transaction
from Testing import ZopeTestCase
from OFS.Folder import manage_addFolder
from Products.BastionLedger.Ledger import manage_addLedger
ZopeTestCase.installProduct('ZScheduler')
ZopeTestCase.installProduct('BastionLedger')
ZopeTestCase.installProduct('BastionBanking')
ZopeTestCase.installProduct('ZCatalog')
ZopeTestCase.installProduct('ZCTextIndex')
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
import time
ledger_name = 'ledger'
ledger_owner = 'ledger_owner'
default_user = ZopeTestCase.user_name

class BankingTestCase(ZopeTestCase.ZopeTestCase):
    """ Base test case for testing BastionLedger functionality """

    def XafterSetUp(self):
        """ hmmm - forcing setup of self.ledger """
        if not getattr(self.app, ledger_name, None):
            manage_addLedger(self.app, ledger_name, 'default', 'test ledger', 'GBP')
        self.ledger = getattr(self.app, ledger_name)
        return

    def X_setupFolder(self):
        pass

    def X_setupUserFolder(self):
        pass

    def X_setupUser(self):
        pass

    def X_login(self):
        pass


def setupBastionLedger(app=None, id=ledger_name, quiet=0):
    if not hasattr(aq_base(app), id):
        _start = time.time()
        quiet or ZopeTestCase._print('Adding BastionLedger instance... ')
    manage_addLedger(app, id, 'test ledger', currency='GBP')
    if not getattr(app, id):
        raise AssertionError('doh ledger not created!')
        if not quiet:
            ZopeTestCase._print('done (%.3fs)\n' % (time.time() - _start,))