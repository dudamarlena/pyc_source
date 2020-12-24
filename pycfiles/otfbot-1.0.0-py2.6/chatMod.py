# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/lib/chatMod.py
# Compiled at: 2011-04-22 06:35:42
""" contains a abstract class for a Bot-module """
from pluginSupport import Plugin

class chatMod(Plugin):
    """
    this class is mainly for documentation of the callbacks.
    some functions are helper functions for common tasks, i.e.
    kicked calls userLeft, so a plugin only implementing userLeft
    will notice that a kicked user left the channel. a plugin implementing
    kicked too, can handle it independent from userLeft, because kicked will
    be overwritten
    """

    def __init__(self, bot):
        self.bot = bot

    def auth(self, user):
        """check the authorisation of the user"""
        pass

    def joined(self, channel):
        """we have joined a channel"""
        pass

    def command(self, user, channel, command, options):
        """a command message received"""
        pass

    def query(self, user, channel, msg):
        """a private message received"""
        pass

    def msg(self, user, channel, msg):
        """message received"""
        pass

    def connectionMade(self):
        """made connection to server"""
        pass

    def connectionLost(self, reason):
        """lost connection to server"""
        pass

    def signedOn(self):
        """successfully signed on"""
        pass

    def left(self, channel):
        """we have left a channel"""
        pass

    def noticed(self, user, channel, msg):
        """we got a notice"""
        pass

    def action(self, user, channel, msg):
        """action (/me) received"""
        pass

    def modeChanged(self, user, channel, set, modes, args):
        """mode changed"""
        pass

    def kickedFrom(self, channel, kicker, message):
        """someone kicked the bot"""
        self.left(channel)

    def userKicked(self, kickee, channel, kicker, message):
        """someone kicked someone else"""
        self.userLeft(kickee, channel)

    def userJoined(self, user, channel):
        """a user joined the channel"""
        pass

    def userJoinedMask(self, user, channel):
        pass

    def userLeft(self, user, channel):
        """a user left the channel"""
        pass

    def userQuit(self, user, quitMessage):
        """a user disconnect from the network"""
        pass

    def yourHost(self, info):
        """info about your host"""
        pass

    def userRenamed(self, oldname, newname):
        """a user changed the nick"""
        pass

    def topicUpdated(self, user, channel, newTopic):
        """a user changed the topic of a channel"""
        pass

    def irc_unknown(self, prefix, command, params):
        """an IRC-Message, which is not handle by twisted was received"""
        pass

    def stop(self):
        """called, when the bot is stopped, or the module is reloaded"""
        pass

    def reload(self):
        """called to reload the settings of the module"""
        pass

    def start(self):
        """called to start the work of the module
            put your initialization stuff in here insteadof __init__
        """
        pass

    def sendLine(self, line):
        pass

    def lineReceived(self, line):
        pass

    def ctcpQuery(self, user, channel, messages):
        """ called for ctcp queries
        """
        pass