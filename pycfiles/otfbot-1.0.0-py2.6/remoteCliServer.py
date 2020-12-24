# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/services/remoteCliServer.py
# Compiled at: 2011-04-22 06:35:42
from twisted.internet import protocol, error, reactor
from twisted.protocols import basic
from twisted.application import service, internet
from twisted.cred import portal, checkers, credentials
from twisted.cred.portal import Portal
from twisted.conch import error, avatar, manhole, recvline, interfaces as conchinterfaces
from twisted.conch.ssh import factory, userauth, connection, keys, session, common
from twisted.conch.insults import insults
from twisted.internet.protocol import ProcessProtocol
from zope.interface import implements
from otfbot.lib.pluginSupport import pluginSupport

class botService(service.MultiService):
    """ 
        This Service should open a port where either a 
        Telnet- or a SSH-Service is listing.
        
        It have to check the authorization of the User,
        who wants to use it. It should provide a verbose
        list of the available Plugins and should manage 
        the textin- and -output. It may also provide a
        Readline-Interface for easier usage.
    """
    name = 'remoteCliServer'

    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        service.MultiService.__init__(self)

    def startService(self):
        self.config = self.parent.getServiceNamed('config')
        f = factory.SSHFactory()
        f.portal = portal.Portal(SSHRealm(self))
        f.publicKeys = {'ssh-rsa': keys.Key.fromString('ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAGEArzJx8OYOnJmzf4tfBEvLi8DVPrJ3/c9k2I/Az64fxjHf9imyRJbixtQhlH9lfNjUIx+4LmrJH5QNRsFporcHDKOTwTTYLh5KmRpslkYHRivcJSkbh/C+BR3utDS555mV')}
        privateKey = '-----BEGIN RSA PRIVATE KEY-----\nMIIByAIBAAJhAK8ycfDmDpyZs3+LXwRLy4vA1T6yd/3PZNiPwM+uH8Yx3/YpskSW\n4sbUIZR/ZXzY1CMfuC5qyR+UDUbBaaK3Bwyjk8E02C4eSpkabJZGB0Yr3CUpG4fw\nvgUd7rQ0ueeZlQIBIwJgbh+1VZfr7WftK5lu7MHtqE1S1vPWZQYE3+VUn8yJADyb\nZ4fsZaCrzW9lkIqXkE3GIY+ojdhZhkO1gbG0118sIgphwSWKRxK0mvh6ERxKqIt1\nxJEJO74EykXZV4oNJ8sjAjEA3J9r2ZghVhGN6V8DnQrTk24Td0E8hU8AcP0FVP+8\nPQm/g/aXf2QQkQT+omdHVEJrAjEAy0pL0EBH6EVS98evDCBtQw22OZT52qXlAwZ2\ngyTriKFVoqjeEjt3SZKKqXHSApP/AjBLpF99zcJJZRq2abgYlf9lv1chkrWqDHUu\nDZttmYJeEfiFBBavVYIF1dOlZT0G8jMCMBc7sOSZodFnAiryP+Qg9otSBjJ3bQML\npSTqy7c3a2AScC/YyOwkDaICHnnD3XyjMwIxALRzl0tQEKMXs6hH8ToUdlLROCrP\nEhQ0wahUTCk1gKA4uPD6TMTChavbh4K63OvbKg==\n-----END RSA PRIVATE KEY-----'
        f.privateKeys = {'ssh-rsa': keys.Key.fromString(privateKey)}
        del privateKey
        try:
            f.portal.checkers = self.root.getServiceNamed('auth').getCheckers()
        except KeyError:
            pass

        serv = internet.TCPServer(int(self.config.get('port', 5022, 'controlTCPMod')), f, interface=self.config.get('interface', '127.0.0.1', 'controlTCPMod'))
        serv.setName('server')
        self.addService(serv)
        service.MultiService.startService(self)


class remoteCLI(pluginSupport, recvline.RecvLine):

    def __init__(self, user):
        """read the list of plugins"""
        self.user = user

    def lineReceived(self, data):
        """ 
            Select the plugin
            pass the data to the selected plugin
            provide a "leave plugin"
        """
        self.terminal.write('Hallo')
        self.terminal.nextLine()
        self.drawInputLine()

    def connectionMade(self):
        """ check the auth of the user and present a list of plugins """
        self.terminal.write('Welcome to the command-line interface to OtfBot')
        self.terminal.nextLine()


class SSHAvatar(avatar.ConchUser):
    implements(conchinterfaces.ISession)

    def __init__(self, username, service):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.service = service
        self.channelLookup.update({'session': session.SSHSession})

    def openShell(self, protocol):
        control = self.service.root.getServiceNamed('control').handle_command
        serverProtocol = insults.ServerProtocol(manhole.ColoredManhole, {'app': self.service.root, 'stop': reactor.stop, 'c': control})
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))

    def getPty(self, terminal, windowSize, attrs):
        return

    def execCommand(self, protocol, cmd):
        raise NotImplementedError

    def closed(self):
        pass


class SSHRealm:
    implements(portal.IRealm)

    def __init__(self, service):
        self.service = service

    def requestAvatar(self, avatarId, mind, *interfaces):
        if conchinterfaces.IConchUser in interfaces:
            return (conchinterfaces.IConchUser, SSHAvatar(avatarId, self.service), lambda : None)
        raise Exception('No supported interfaces found.')