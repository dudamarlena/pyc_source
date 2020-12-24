# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/services/ircServer.py
# Compiled at: 2011-04-22 06:35:42
from twisted.internet import reactor, protocol
from twisted.internet.tcp import Server
from twisted.words.protocols.irc import IRC
from twisted.words.protocols import irc
from twisted.words.service import IRCUser
from twisted.application import service, internet
import logging, traceback, sys, time, glob, traceback
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport import pluginSupport

class MyTCPServer(internet.TCPServer):
    """
        TCPServer, which has self.root, self.parent and self.factory
    """

    def __init__(self, root, parent, *args, **kwargs):
        self.root = root
        self.parent = parent
        self.factory = kwargs['factory']
        internet.TCPServer.__init__(self, *args, **kwargs)


class botService(service.MultiService):
    """
        botService spawning MYTCPServer instances using Server as protocol
    """
    name = 'ircServer'

    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.instances = []
        service.MultiService.__init__(self)

    def startService(self):
        try:
            self.config = self.root.getServiceNamed('config')
            port = int(self.config.get('port', '6667', 'server'))
            interface = interface = self.config.get('interface', '127.0.0.1', 'server')
            factory = ircServerFactory(self.root, self)
            serv = MyTCPServer(self.root, self, port=port, factory=factory, interface=interface)
            self.addService(serv)
            service.MultiService.startService(self)
        except Exception, e:
            logger = logging.getLogger('server')
            logger.error(e)
            tb_list = traceback.format_tb(sys.exc_info()[2])[1:]
            for entry in tb_list:
                for line in entry.strip().split('\n'):
                    logger.error(line)


class Server(IRCUser, pluginSupport):
    """
        the server protocol, implemending pluginSupport and IRCUser
    """
    pluginSupportName = 'ircServer'
    pluginSupportPath = 'otfbot/plugins/ircServer'

    def __init__(self, root, parent):
        pluginSupport.__init__(self, root, parent)
        self.name = 'nickname'
        self.user = 'user'
        self.loggedon = False
        self.logger = logging.getLogger('server')
        self.classes = []
        self.config = root.getServiceNamed('config')
        self.startPlugins()

    def handleCommand(self, command, prefix, params):
        """Determine the function to call for the given command and call
        it with the given arguments.
        """
        self._apirunner('irc_%s' % command, {'prefix': prefix, 'params': params})

    def connectionMade(self):
        self._apirunner('connectionMade')
        self.logger.info('connection made')
        self.connected = True

    def connectionLost(self, reason):
        self.connected = False
        self.parent.instances.remove(self)

    def getHostmask(self):
        return '%s!%s@%s' % (self.name, self.user, self.hostname)

    def sendmsg(self, user, channel, msg):
        if self.connected:
            self.privmsg(user, channel, msg)

    def action(self, user, channel, msg):
        if self.connected:
            self.sendLine(':%s PRIVMSG %s :ACTION %s' % (user, channel, msg))

    def stop(self):
        self._apirunner('stop')
        for mod in self.plugins.keys():
            del self.plugins[mod]

        self.plugins = {}


class ircServerFactory(protocol.ServerFactory):
    """
        Factory building Server instaces, used by twisted
    """

    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.config = root.getServiceNamed('config')
        self.protocol = Server

    def buildProtocol(self, addr):
        """ 
            builds the protocol and appends the instance to parent.intances

            @return: the instance
        """
        p = self.protocol(self.root, self.parent)
        self.parent.instances.append(p)
        return p