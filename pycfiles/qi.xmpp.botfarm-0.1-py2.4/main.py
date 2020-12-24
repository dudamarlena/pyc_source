# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/xmpp/botfarm/main.py
# Compiled at: 2008-08-08 08:15:00
from twisted.application import service
from twisted.web import server
from twisted.internet import reactor
import twisted.python.log as log
from sys import stdout, argv
import qi.xmpp.botfarm.config as config
from qi.xmpp.botfarm.xmlConfig import loadConfigFile
from qi.xmpp.botfarm.xmlrpc import XMLRPCServer
from sessionManager import SessionManager

class App:
    __module__ = __name__

    def __init__(self):
        """
                """
        log.startLogging(stdout)
        sessionManager = SessionManager()
        sessionManager.loadAdminSession()
        xrs = XMLRPCServer(sessionManager)
        reactor.listenTCP(config.xmlrpc_port, server.Site(xrs))
        reactor.addSystemEventTrigger('before', 'shutdown', sessionManager.unloadSessions)


def main():
    """
        """
    if len(argv) != 2:
        print 'You need to specify the configuration file.'
        return
    loadConfigFile(argv[1])
    app = App()
    reactor.run()


if __name__ == '__main__':
    main()