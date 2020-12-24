# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/signableevent/utils.py
# Compiled at: 2011-07-29 07:55:08
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser

class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id."""

    def getId(self):
        """Return the ID of the user."""
        return self.getUserName()


def run_as_manager(self, callback, *args, **kwargs):
    """
    Run the given function as a manager user

    self must be an acquisition context able to locate acl_users
    """
    tmp_user = UnrestrictedUser('manager', '', ['Manager'], '')
    tmp_user = tmp_user.__of__(self.acl_users)
    old_sm = getSecurityManager()
    try:
        newSecurityManager(None, tmp_user)
        return callback(*args, **kwargs)
    finally:
        setSecurityManager(old_sm)

    return