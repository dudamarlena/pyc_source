# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/anymeta/manhole.py
# Compiled at: 2011-01-19 13:57:12
__doc__ = "\nCommon manhole service for anymeta applications.\n\nThis provides a factory to set up a manhole. A typical use is:\n\n    manholeFactory = manhole.getFactory(namespace, admin='admin')\n    manholeService = strports.service('tcp:2222:interface=127.0.0.1',\n                                      manholeFactory)\n\nIt is highly recommended to only allow access from the loopback interface.\n"
from twisted.cred import portal, checkers
from twisted.conch.insults import insults
from twisted.conch import manhole, manhole_ssh

def getFactory(namespace, **passwords):
    """
    Return a protocol factory to set up an ssh manhole.

    @param namespace: The initial global variables accessible in the
        interactive shell.
    @param passwords: This allows for providing username and password
        combinations as keyword arguments.
    """

    class chainedProtocolFactory:

        def __init__(self, namespace):
            self.namespace = namespace

        def __call__(self):
            return insults.ServerProtocol(manhole.ColoredManhole, self.namespace)

    checker = checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords)
    sshRealm = manhole_ssh.TerminalRealm()
    sshRealm.chainedProtocolFactory = chainedProtocolFactory(namespace)
    sshPortal = portal.Portal(sshRealm, [checker])
    return manhole_ssh.ConchFactory(sshPortal)