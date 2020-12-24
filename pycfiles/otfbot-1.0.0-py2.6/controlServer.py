# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircServer/controlServer.py
# Compiled at: 2011-04-22 06:35:42
from twisted.internet import reactor
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback
import time

class Plugin(chatMod.chatMod):

    def __init__(self, server):
        self.server = server
        self.first = True

    @callback
    def irc_NICK(self, prefix, params):
        if self.first:
            if not self.server.loggedon:
                return
            self.server.join(self.server.getHostmask(), '#control')
            self.server.privmsg(self.server.getHostmask(), '#control', 'Welcome to the OTFBot control channel. Type "help" for help ;).')
            self.server.names(self.server.name, '#control', ['OtfBot', self.server.name])

    @callback
    def irc_PRIVMSG(self, prefix, params):
        channel = params[0]
        if channel == '#control':
            msg = params[1]
            for server in self.server.factory.instances:
                self.logger.debug(self.server.getHostmask())
                server.privmsg(self.server.getHostmask(), '#control', msg)

            response = self.server.root.getServiceNamed('control').handle_command(msg)
            if not response:
                return
            if not type(response) == list:
                response = [
                 response]
            for resp in response:
                for line in resp.split('\n'):
                    self.server.privmsg(self.server.getHostmask(), '#control', line)