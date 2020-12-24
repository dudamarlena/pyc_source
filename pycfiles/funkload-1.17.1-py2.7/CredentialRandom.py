# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/CredentialRandom.py
# Compiled at: 2015-05-06 05:03:08
"""A random credential server/controller.

$Id$
"""
import sys
from Lipsum import Lipsum
from XmlRpcBase import XmlRpcBaseServer, XmlRpcBaseController
from CredentialBase import CredentialBaseServer

class CredentialRandomServer(XmlRpcBaseServer, CredentialBaseServer):
    """A random credential server."""
    server_name = 'random_credential'
    method_names = XmlRpcBaseServer.method_names + [
     'getCredential', 'listCredentials', 'listGroups']

    def __init__(self, argv=None):
        XmlRpcBaseServer.__init__(self, argv)
        self.lipsum = Lipsum()

    def getCredential(self, group=None):
        """Return a random (login, password).

        return a random user login, the login is taken from the lipsum
        vocabulary so the number of login is limited to the length of the
        vocabulary. The group asked will prefix the login name.

        The password is just the reverse of the login, this give a coherent
        behaviour if it return twice the same credential.
        """
        self.logd('getCredential(%s) request.' % group)
        user = (group or 'user') + '_' + self.lipsum.getWord()
        tmp = list(user)
        tmp.reverse()
        password = ('').join(tmp)
        self.logd('  return (%s, %s)' % (user, password))
        return (user, password)

    def listCredentials(self, group=None):
        """Return a list of 10 random credentials."""
        self.logd('listCredentials request.')
        return [ self.getCredential(group) for x in range(10) ]

    def listGroups(self):
        """Retrun a list of 10 random group name."""
        self.logd('listGroups request.')
        lipsum = self.lipsum
        return [ 'grp' + lipsum.getUniqWord(length_min=2, length_max=3) for x in range(10)
               ]


class CredentialRandomController(XmlRpcBaseController):
    """A random credential controller."""
    server_class = CredentialRandomServer

    def test(self):
        """Testing credential server."""
        server = self.server
        self.log(server.listGroups())
        for i in range(10):
            self.log('%s getCredential() ... ' % i)
            user, password = server.getCredential()
            self.log(' return (%s, %s)\n' % (user, password))

        for group in server.listGroups():
            self.log('group %s\n' % group)
            self.log('  content: %s\n' % server.listCredentials(group))

        return 0


def main():
    """Control credentiald server."""
    ctl = CredentialRandomController()
    sys.exit(ctl())


if __name__ == '__main__':
    main()