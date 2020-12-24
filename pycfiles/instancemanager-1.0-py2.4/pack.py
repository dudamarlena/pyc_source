# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/instancemanager/pack.py
# Compiled at: 2007-12-17 05:32:50
"""Script that packs the database.

You can pass it an argument for the number of days of transactions to
keep in the database.
"""
import sys
try:
    from AccessControl.SecurityManagement import newSecurityManager
except:
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(0)
    else:
        raise

from AccessControl.SecurityManager import setSecurityPolicy
from Products.CMFCore.tests.base.security import OmnipotentUser
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy
from Testing.makerequest import makerequest
import transaction

class Packer:
    __module__ = __name__

    def __init__(self, app):
        """Read the command line parameters and initialise.
        """
        self.app = app
        _policy = PermissiveSecurityPolicy()
        _oldpolicy = setSecurityPolicy(_policy)
        newSecurityManager(None, OmnipotentUser().__of__(self.app.acl_users))
        self.app = makerequest(self.app)
        arguments = sys.argv[1:]
        if len(arguments) < 1:
            sys.exit('Not enough arguments.')
        self.days = arguments[0]
        self.days = int(self.days)
        return

    def run(self):
        """Perform the actual process.
        """
        main = app.Control_Panel.Database['main']
        main.manage_pack(days=self.days)


packer = Packer(app)
packer.run()