# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircServer/human.py
# Compiled at: 2011-04-22 06:35:42
from twisted.internet import protocol, reactor
from twisted.words.protocols import irc
from twisted.words import service
from twisted.protocols import basic
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback
import string

def sendNames(server, network, channel):
    getClient = lambda network: server.root.getServiceNamed('ircClient').namedServices[network].factory.protocol
    if network in server.root.getServiceNamed('ircClient').namedServices.keys():
        ircClient = server.root.getServiceNamed('ircClient')
        users = ircClient.namedServices[network].factory.protocol.getUsers(channel)
        names = [ user.nick for user in users ]
        server.names(server.name, '#' + network + '-' + channel, names)


class Plugin(chatMod.chatMod):

    def __init__(self, server):
        server.depends_on_service('ircClient')
        self.server = server
        self.mychannels = []
        self.first = True
        self.getClient = lambda network: server.root.getServiceNamed('ircClient').getServiceNamed(network).protocol
        self.getClientNames = lambda : [ connection.name for connection in self.server.root.getServiceNamed('ircClient').services ]
        self.server.registerCallback(self, 'irc_NICK')
        self.server.registerCallback(self, 'irc_PRIVMSG')
        self.server.registerCallback(self, 'irc_JOIN')
        self.server.registerCallback(self, 'irc_PART')

    @callback
    def irc_NICK(self, prefix, params):
        if not self.first:
            return
        if not self.server.loggedon:
            return
        self.first = False
        for network in self.getClientNames():
            bot = self.getClient(network)
            for channel in bot.channels:
                self.server.join(self.server.getHostmask(), '#' + network + '-' + channel)
                sendNames(self.server, network, channel)
                self.mychannels.append('#' + network + '-' + channel)

    @callback
    def irc_PRIVMSG(self, prefix, params):
        if params[0][0] == '#':
            if params[0] in self.mychannels:
                (network, channel) = params[0][1:].split('-', 1)
                self.getClient(network).sendmsg(channel, params[1])
        elif '-' in params[0]:
            (network, nick) = params[0].split('-', 1)
            self.getClient(network).sendmsg(nick, params[1])

    @callback
    def irc_JOIN(self, prefix, params):
        try:
            (network, channel) = params[0][1:].split('-', 1)
            if network in self.getClientNames():
                if len(params) >= 2:
                    self.server.root.getServiceNamed('config').set('password', params[1], 'main', network, channel)
                    self.getClient(network).join(channel, params[1])
                else:
                    self.getClient(network).join(channel)
                self.server.join(self.server.getHostmask(), '#%s-%s' % (network, channel))
                if channel in self.getClient(network).users.keys():
                    sendNames(self.server, network, channel)
                self.mychannels.append('#%s-%s' % (network, channel))
        except ValueError:
            pass

    @callback
    def irc_PART(self, prefix, params):
        try:
            (network, channel) = params[0][1:].split('-', 1)
            if network in self.getClientNames():
                self.getClient(network).part(channel)
                self.server.part(self.server.getHostmask(), '#%s-%s' % (network, channel))
                self.mychannels.remove('#%s-%s' % (network, channel))
        except ValueError:
            pass