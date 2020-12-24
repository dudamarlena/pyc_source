# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/simpleserver/http/manhole.py
# Compiled at: 2007-07-25 20:13:09
"""
An interactive Python interpreter with syntax coloring.
 
Nothing interesting is actually defined here.  Two listening ports are
set up and attached to protocols which know how to properly set up a
ColoredManhole instance.
"""
from twisted.conch.manhole import ColoredManhole
from twisted.conch.insults import insults
from twisted.conch.telnet import TelnetTransport, TelnetBootstrapProtocol
from twisted.conch.manhole_ssh import ConchFactory, TerminalRealm
from twisted.internet import protocol
from twisted.application import internet, service
from twisted.cred import checkers, portal

def makeService(port, interface, username, password, namespace):
    checker = checkers.InMemoryUsernamePasswordDatabaseDontUse(**{username: password})

    def chainProtocolFactory():
        return insults.ServerProtocol(ColoredManhole, namespace)

    rlm = TerminalRealm()
    rlm.chainedProtocolFactory = chainProtocolFactory
    ptl = portal.Portal(rlm, [checker])
    f = ConchFactory(ptl)
    return internet.TCPServer(port, f, interface=interface)