# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/lib/user.py
# Compiled at: 2011-04-22 06:35:42
"""
    Objects to represent users
"""
from twisted.words import service
import hashlib

class BotUser(service.User):
    """ represents a user of the bot

        @ivar password: Authentification data
        @ivar ircuser: references to IrcUser instances
    """
    password = ''
    ircuser = {}

    def __init__(self, name):
        self.name = name

    def setPasswd(self, passwd):
        """
            update the password

            takes a string as password and stores the hash.

            @param passwd: the new password.
            @type passwd: string
        """
        self.password = self._hashpw(passwd)

    def checkPasswd(self, passwd):
        """
            checks if the password for the user equals passwd

            @param passwd: input password
            @type passwd: string
            @returns: true if the password was correct
        """
        return self._hashpw(passwd) == self.password

    def _hashpw(self, pw):
        s = hashlib.sha1(pw)
        return s.hexdigest()

    def __repr__(self):
        return '<BotUser %s>' % self.name


MODE_CHARS = {' ': 0, 
   'v': 1, 
   'h': 2, 
   'o': 4, 
   'a': 8, 
   'q': 16}
MODE_SIGNS = {0: ' ', 
   1: '+', 
   2: 'h', 
   4: '@', 
   8: '!', 
   16: '&'}

class IrcUser(object):
    """ Represents the connection of a L{BotUser} via IRC

        @ivar network: reference to the network over which
                        the user is connected
        @ivar name:    verbose name of this connection
        @ivar nick:    IRC nick
        @ivar user:    user part of the hostmask
        @ivar host:    host part of the hostmask
        @ivar avatar:  reference to the corresponding L{BotUser}
                       instance
        @ivar realname: content of the realname property of the user
    """

    def __init__(self, nick, user, host, realname, network):
        self.network = network
        self.name = 'anonymous'
        self.nick = nick
        self.user = user
        self.host = host
        self.avatar = None
        self.realname = realname
        self.channels = set()
        self.modes = {}
        return

    def getBotuser(self):
        return self.avatar

    def setBotuser(self, avatar):
        self.avatar = avatar

    def hasBotuser(self):
        return self.avatar != None

    def setNick(self, nick):
        self.nick = nick

    def setChannels(self, channels):
        """ set the channels list to the set given as parameter
            @ivar channels: the channellist
        """
        self.channels = set([ channel.lower() for channel in channels ])
        for channel in self.channels:
            self.modes[channel] = 0

    def getChannels(self):
        """ get the channels list """
        return self.channels

    def addChannel(self, channel):
        """ add a channel to the list of channels of the user
            @ivar channel: the channel to add
        """
        assert type(channel) == str
        self.channels.add(channel.lower())
        self.modes[channel] = 0

    def hasChannel(self, channel):
        return channel.lower() in self.channels

    def removeChannel(self, channel):
        """ remove a channel from the list of channels
            @ivar channel: the channel to remove
        """
        channel = channel.lower()
        if channel not in self.channels:
            return
        self.channels.remove(channel)
        del self.modes[channel]

    def setMode(self, channel, modechar):
        """ set the usermode specified by the char modchar on channel
            @ivar channel: the channel where the mode is set
            @ivar modechar: the char corrosponding to the mode (i.e. "o")
        """
        channel = channel.lower()
        assert channel in self.channels
        assert modechar in MODE_CHARS
        assert channel in self.modes
        self.modes[channel] = self.modes[channel] | MODE_CHARS[modechar]

    def removeMode(self, channel, modechar):
        """ remove the usermode specified by the char modchar on channel
            @ivar channel: the channel where the mode is removed
            @ivar modechar: the char corrosponding to the mode (i.e. "o")
        """
        channel = channel.lower()
        assert channel in self.channels
        assert modechar in MODE_CHARS
        all_set = reduce(lambda x, y: x + y, MODE_CHARS.values())
        self.modes[channel] = self.modes[channel] & (all_set ^ MODE_CHARS[modechar])

    def getModeSign(self, channel):
        channel = channel.lower()
        assert channel in self.channels
        ret_sign = ''
        for sign in MODE_SIGNS:
            if self.modes[channel] & sign:
                ret_sign = MODE_SIGNS[sign]

        return ret_sign

    def getHostMask(self):
        return self.nick + '!' + self.user + '@' + self.host

    def getNick(self):
        return self.nick

    def getUsername(self):
        return self.user

    def getHost(self):
        return self.host

    def __repr__(self):
        return '<IrcUser %s (%s)>' % (self.getHostMask(), self.name)

    def __str__(self):
        return self.getHostMask()