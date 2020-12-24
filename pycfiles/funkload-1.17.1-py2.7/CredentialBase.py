# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/CredentialBase.py
# Compiled at: 2015-05-06 05:03:08
"""Interface of a Credential Server.

$Id$
"""

class CredentialBaseServer:
    """Interface of a Credential server."""

    def getCredential(self, group=None):
        """Return a credential (login, password).

        If group is not None return a credential that belong to the group.
        """
        pass

    def listCredentials(self, group=None):
        """Return a list of all credentials.

        If group is not None return a list of credentials that belong to the
        group.
        """
        pass

    def listGroups(self):
        """Return a list of all groups."""
        pass