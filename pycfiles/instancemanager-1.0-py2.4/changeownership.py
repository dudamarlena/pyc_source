# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/instancemanager/changeownership.py
# Compiled at: 2007-12-17 05:32:50
"""Script that changes the ownership of some documents

This looks in the catalog for content with originalOwner as Creator.
That should suffice for most cases and is a lot faster than waking up
every object in the database and asking it for its owner.

The ownership of every object found is given to newOwner.

This is for instance handy when you used an older version of
instancemanager to create a plone site.  This would initially make
that site as the non-existing user 'all_powerful_Oz'.  See
https://dev.plone.org/plone/ticket/5727

With this script you can change the ownership of that content to
e.g. the user 'admin'.

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

class ChangeOwner:
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
        if len(arguments) < 2:
            sys.exit('Not enough arguments.')
        self.ploneSiteName = arguments[0]
        self.originalOwner = arguments[1]
        self.newOwner = arguments[2]
        return

    def run(self):
        """Perform the actual process.
        """
        from StringIO import StringIO
        out = StringIO()
        print >> out, 'Starting change of ownership...'
        from Products.CMFCore.utils import getToolByName
        context = self.app[self.ploneSiteName]
        plone_tool = getToolByName(context, 'plone_utils')
        results = context.portal_catalog.searchResults(Creator=self.originalOwner)
        if len(results) > 0:
            print >> out, '%s owns %d documents.  Giving them to %s.' % (self.originalOwner, len(results), self.newOwner)
            for item in results:
                obj = item.getObject()
                print >> out, 'Changing owner of', obj.title_or_id()
                plone_tool.changeOwnershipOf(obj, self.newOwner)
                obj.setCreators(self.newOwner)
                transaction.commit()

        else:
            print >> out, 'No ownership changed.'
        return out.getvalue()


chown = ChangeOwner(app)
log = chown.run()
print log