# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircServer/basic.py
# Compiled at: 2011-04-22 06:35:42
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback, callback_with_priority
from twisted.words.protocols import irc

class Plugin(chatMod.chatMod):

    def __init__(self, server):
        self.server = server

    @callback
    def irc_PING(self, prefix, params):
        self.server.sendMessage('PONG', ':' + params[0])

    @callback
    def irc_USER(self, prefix, params):
        self.server.user = params[0]
        self.server.hostname = params[2]
        self.server.realname = params[3]

    @callback_with_priority(100)
    def irc_NICK(self, prefix, params):
        for server in self.server.parent.instances:
            if server.name == params[0] and server != self.server:
                self.server.sendMessage(irc.ERR_NICKNAMEINUSE, 'nickname already in use', prefix='localhost')
                return

        self.server.name = params[0]
        if not self.server.loggedon:
            self.server.sendMessage(irc.RPL_WELCOME, ':connected to OTFBot IRC', prefix='localhost')
            self.server.sendMessage(irc.RPL_YOURHOST, ':Your host is %(serviceName)s, running version %(serviceVersion)s' % {'serviceName': self.server.transport.server.getHost(), 'serviceVersion': 'VERSION'}, prefix='localhost')
            self.server.sendMessage(irc.RPL_MOTD, ':Welcome to the Bot-Control-Server', prefix='localhost')
            self.server.loggedon = True

    @callback
    def irc_QUIT(self, prefix, params):
        self.server.connected = False