# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/services/ircClient.py
# Compiled at: 2011-04-22 06:35:42
"""
    Providing a client interface to IRC
"""
from twisted.application import internet, service
from twisted.internet import protocol, reactor, error, ssl
from twisted.words.protocols import irc
import logging, string, time
from threading import Lock
import gettext, traceback
from otfbot.lib.pluginSupport import pluginSupport
from otfbot.lib.user import IrcUser, MODE_CHARS, MODE_SIGNS

class Meta:
    depends = [
     'auth', 'control', 'scheduler']


def syncedChannel(argnum=None):

    def decorator(func):

        def callSynced(self, *args, **kwargs):
            if 'channel' in kwargs:
                channel = kwargs['channel']
            elif argnum:
                channel = args[argnum]
            else:
                channel = ''
                self.logger.error('Decorator has no channel property!')
            if channel in self.syncing_channels:
                self.callback_queue.append(([channel], (func, args, kwargs)))
            else:
                func(self, *args, **kwargs)

        return callSynced

    return decorator


def syncedChannelRaw(func):

    def callSynced(self, *args, **kwargs):
        assert len(args) >= 2
        channel = args[1][(-1)]
        if channel in self.syncing_channels:
            self.callback_queue.append(([channel], (func, args, kwargs)))
        else:
            func(self, *args, **kwargs)

    return callSynced


def syncedAll(func):

    def callSynced(self, *args, **kwargs):
        if len(self.syncing_channels):
            self.callback_queue.append((self.syncing_channels, (func, args, kwargs)))
        else:
            func(self, *args, **kwargs)

    return callSynced


class botService(service.MultiService):
    name = 'ircClient'

    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        service.MultiService.__init__(self)

    def startService(self):
        """ 
        start the service

        registers control-commands, connects to the configured networks
        and then calls MultiService.startService

        """
        self.controlservice = self.root.getServiceNamed('control')
        self.logger = logging.getLogger(self.name)
        self.config = self.root.getServiceNamed('config')
        if not self.controlservice:
            logger.warning('cannot register control-commands as ' + 'no control-service is available')
        else:
            self.register_ctl_command(self.connect)
            self.register_ctl_command(self.disconnect)
            self.register_ctl_command(lambda : self.namedServices.keys(), name='list')
        for network in self.config.getNetworks():
            if self.config.getBool('enabled', False, 'main', network):
                self.connect(network)

        service.MultiService.startService(self)

    def connect(self, network):
        """
            connect to the network
            @ivar network: the name of the network to connect to as used in the config

            gets the servername and port from config, and then connects to the network.
        """
        f = BotFactory(self.root, self, network)
        sname = self.config.get('server', 'localhost', 'main', network)
        port = int(self.config.get('port', 6667, 'main', network))
        if self.config.getBool('ssl', False, 'main', network):
            s = ssl.ClientContextFactory()
            serv = internet.SSLClient(host=sname, port=port, factory=f, contextFactory=s)
            repr = '<IRC Connection with SSL to %s:%s>'
            serv.__repr__ = lambda : repr % (sname, port)
            serv.factory = f
        else:
            serv = internet.TCPClient(host=sname, port=port, factory=f)
            serv.__repr__ = lambda : '<IRC Connection to %s:%s>' % (sname, port)
            serv.factory = f
        f.service = serv
        serv.setName(network)
        serv.parent = self
        self.config.set('enabled', True, 'main', network)
        self.addService(serv)

    def disconnect(self, network):
        """
            manually disconnect from a network 
            @param network: the networkname
            @type network: str
        """
        if network in self.namedServices:
            self.namedServices[network].protocol.disconnect()
            self.removeService(self.namedServices[network])
            self.config.set('enabled', False, 'main', network)
            return 'Disconnected from ' + network
        else:
            return 'Not connected to ' + network

    def register_ctl_command(self, f, namespace=None, name=None):
        if self.controlservice:
            if namespace is None:
                namespace = []
            if not type(namespace) == list:
                namespace = [
                 namespace]
            namespace.insert(0, self.name)
            self.controlservice.register_command(f, namespace, name)
        return


class BotFactory(protocol.ReconnectingClientFactory):
    """The Factory for the Bot"""

    def __init__(self, root, parent, network):
        self.root = root
        self.parent = parent
        self.protocolClass = Bot
        self.network = network
        self.config = root.getServiceNamed('config')
        self.logger = logging.getLogger(network)
        self.stop = False

    def __repr__(self):
        return '<BotFactory for network %s>' % self.network

    def startedConnecting(self, connector):
        """ callback invoced when connecting is started. logs it. """
        self.logger.info('Started to connect')

    def clientConnectionLost(self, connector, reason):
        """ 
        callback invoced when connection is lost.

        tries to reconnect or disconnects cleanly.
        """
        self.protocol = None
        self.service.protocol = None
        if not self.stop:
            mstr = 'Got disconnected from %s: %s'
            self.logger.warn(mstr % (connector.host, reason.getErrorMessage()))
            protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        else:
            self.parent.removeService(self.service)
        return

    def clientConnectionFailed(self, connector, reason):
        mstr = 'Connection to %s failed: %s'
        self.logger.warn(mstr % (connector.host, reason.getErrorMessage()))
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def buildProtocol(self, addr):
        proto = self.protocolClass(self.root, self)
        self.protocol = proto
        self.service.protocol = proto
        self.resetDelay()
        return proto

    def allow_disconnect(self):
        """
            stops the factory from reconnecting after disconnect
        """
        self.stop = True


class Bot(pluginSupport, irc.IRCClient):
    """ The Protocol of our IRC-Bot
        @ivar plugins: contains references to all plugins, which are loaded
        @type plugins: list
        @ivar channels: all channels we are currently in
        @type channels: list
        @ivar network: the name of the network we are connected to
        @type network: string
        @ivar logger: a instance of the standard python logger
        @ivar nickname: the nick of the bot
    """
    pluginSupportPath = 'otfbot/plugins/ircClient'
    pluginSupportName = 'ircClient'
    sourceURL = 'http://www.otfbot.org/download/'
    erroneousNickFallback = 'otfbot'
    modchars = {16: 'a', 8: 'o', 4: 'h', 2: 'v', 0: ' '}
    modcharvals = {16: '!', 8: '@', 4: '%', 2: '+', 0: ' '}

    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.config = root.getServiceNamed('config')
        self.network = self.parent.network
        self.ircClient = self.parent.parent
        self.factory = parent
        self.logger = logging.getLogger(self.network)
        pluginSupport.__init__(self, root, parent)
        if self.config.getBool('answerToCTCPVersion', True, 'main', self.network):
            self.versionName = 'OTFBot'
            self.versionNum = root.version.short()
            self.versionEnv = ''
        self.channels = []
        self.realname = self.config.get('realname', 'A Bot', 'main', self.network)
        self.password = self.config.get('password', None, 'main', self.network)
        self.nickname = self.config.get('nickname', 'OtfBot', 'main', self.network)
        self.nickname = unicode(self.nickname).encode('iso-8859-1')
        self.hostmask = ''
        self.channels = self.config.getChannels(self.network) or []
        self.lineRate = 1.0 / float(self.config.get('linesPerSecond', '2', 'main', self.network))
        self.user_list = {}
        self.mymodes = {}
        self.channelmodes = {}
        self.serversupports = {}
        self.translations = {}
        self.syncing_channels = []
        self.callback_queue = []
        self.sync_lock = Lock()
        self.logger.info('Starting new Botinstance')
        self.startPlugins()
        self.register_my_commands()
        self.startTimeoutDetection()
        return

    def _synced_apirunner(self, apifunction, args={}):
        assert 'channel' in args, args
        channel = args['channel']
        if channel in self.syncing_channels:
            self.callback_queue.append(([channel], (self._apirunner, (apifunction, args), {})))
        else:
            self._apirunner(apifunction, args)

    def handleCommand(self, command, prefix, params):
        """ 
        same as twisteds, only with reasonable logging in case of exceptions
 
        Determine the function to call for the given command and call it with
        the given arguments.
        """
        method = getattr(self, 'irc_%s' % command, None)
        try:
            if method is not None:
                method(prefix, params)
            else:
                self.irc_unknown(prefix, command, params)
        except Exception, e:
            self.logerror(self.logger, self.pluginSupportName, e)

        return

    def startTimeoutDetection(self):
        """ initialize the timeout-detection scheduler-call """
        self.lastLine = time.time()
        scheduler = self.root.getServiceNamed('scheduler')
        scheduler.callPeriodic(60, self._check_sendLastLine)

    def getUsers(self, channel=None):
        """ Get a list of users in channel (or all channels if channel=None)
            @rtype: dict
            @return: a list of users
        """
        ret = []
        if not channel:
            return self.user_list.values()
        for user in self.user_list:
            if self.user_list[user].hasChannel(channel):
                ret.append(self.user_list[user])

        return ret

    def getUserByNick(self, nick):
        for user in self.user_list.values():
            if user.nick.lower() == nick.lower():
                return user

        return

    def _check_sendLastLine(self):
        timeout = self.config.get('timeout', 120, 'main', self.network)
        if time.time() - self.lastLine > timeout:
            self.ping()
        return True

    def register_ctl_command(self, f, namespace=None, name=None):
        if not self.controlservice:
            return
        else:
            if namespace is None:
                namespace = []
            if not type(namespace) == list:
                namespace = list(namespace)
            namespace.insert(0, self.network)
            self.ircClient.register_ctl_command(f, namespace, name)
            return

    def register_my_commands(self):
        self.register_ctl_command(self.join)
        self.register_ctl_command(self.leave, name='part')
        self.register_ctl_command(self.getUsers)
        self.register_ctl_command(self.setNick, name='rename')
        self.register_ctl_command(lambda : self.channels, name='listchannels')
        self.register_ctl_command(self.kick)
        self.register_ctl_command(self.sendmsg, name='say')
        self.register_ctl_command(self.ping)

    def getFactory(self):
        """ get the factory
            @rtype: BotFactory
            @return: the current factory
        """
        return self.factory

    def auth(self, user):
        """
            call this, to see which rights C{user} has
            @type user: string
            @param user: the full hostmask of the user
            @rtype: int
            @return: the level of access rights (0 = nothing, 10 = everything)
        """
        level = 0
        for plugin in self.plugins.values():
            if hasattr(plugin, 'auth'):
                level = max(plugin.auth(user), level)

        return level

    def encode_line(self, line, encoding, fallback):
        """
            encode a line, trying to use encoding, falling back to fallback
            @ivar line: the line to encode
            @ivar encoding: the assumed encoding (i.e. UTF-8)
            @ivar fallback: a safe fallback (i.e. iso-8859-15)
        """
        enc = self.config.get('encoding', 'UTF-8', 'main')
        if not type(line) == unicode:
            if self.config.getBool('debugUnicode', False):
                self.logger.debug('output line is not an unicode object')
                for l in traceback.format_stack(limit=6):
                    for l2 in l.split('\n'):
                        if l2.strip():
                            self.logger.debug(l2)

            try:
                line = unicode(line, encoding)
            except UnicodeDecodeError:
                line = unicode(line, fallback, errors='replace')

        line = line.encode(enc)
        return line

    def get_gettext(self, channel=None):
        lang = self.config.get('language', None, 'main', self.network, channel)
        if lang not in self.translations and lang:
            if gettext.find('otfbot', 'locale', languages=[lang]):
                self.translations[lang] = gettext.translation('otfbot', 'locale', languages=[
                 lang])
            else:
                lang = None
        if lang:

            def _(input):
                return self.translations[lang].ugettext(input)

        else:

            def _(input):
                return input

        return _

    def sendmsg(self, channel, msg, encoding='UTF-8', fallback='iso-8859-15'):
        """
            call B{only} this to send messages to channels or users
            it converts the message from iso-8859-15 to a encoding given
            in the config
            @type     channel:     string
            @param    channel:     send the message to this channel or user
            @type     msg:         string
            @param    msg:         the message to send
            @type     encoding:    string
            @param    encoding:    the encoding of C{msg}
            @type     fallback:    string
            @param    fallback:    try this one as encoding for C{msg},
                                   if C{encoding} doesn't work
        """
        if not type(msg) == list:
            msg = [
             msg]
        for line in msg:
            line = self.encode_line(line, encoding, fallback)
            self.msg(channel, line, 450)
            self.privmsg(self.nickname, channel, line)

    def sendme(self, channel, action, encoding='UTF-8', fallback='iso8859-15'):
        """
            call B{only} this to send actions (/me) to channels
            it converts the message from iso-8859-15 to a encoding given
            in the config
            @type    channel:    string
            @param    channel:    send the message to this channel or user
            @type    action:        string
            @param    action:        the message to send
            @type    encoding:    string
            @param    encoding:    the encoding of C{msg}
            @param    fallback:    the encoding of C{msg}
        """
        if not type(action) == list:
            action = [
             action]
        for line in action:
            line = self.encode_line(line, encoding, fallback)
            self.describe(channel, line)
            self.action(self.nickname, channel, line)

    def join(self, channel, key=None):
        """
            wrapper around IRCClient.join, which only allows proper channels
        """
        if channel[0] not in irc.CHANNEL_PREFIXES:
            self.logger.error('cannot join "%s", because it is not a channel' % channel)
            return
        return irc.IRCClient.join(self, channel, key)

    def leave(self, channel, reason=None):
        """
            wrapper around IRCClient.leave, which only allows proper channels
        """
        if channel[0] not in irc.CHANNEL_PREFIXES:
            self.logger.error('cannot leave "%s", because it is not a channel' % channel)
            return
        return irc.IRCClient.leave(self, channel, reason)

    def kick(self, channel, user, reason=None):
        """
            wrapper around IRCClient.kick, which only allows proper channels
        """
        if channel[0] not in irc.CHANNEL_PREFIXES:
            self.logger.error('cannot kick user from "%s", because it is not a channel' % channel)
            return
        return irc.IRCClient.kick(self, channel, user, reason)

    def topic(self, channel, topic=None):
        """
            wrapper around IRCClient.topic, which only allows proper channels
        """
        if channel[0] not in irc.CHANNEL_PREFIXES:
            self.logger.error('cannot change topic of "%s", because it is not a channel' % channel)
            return
        return irc.IRCClient.topic(self, channel, topic)

    def connectionMade(self):
        """
            this is called by twisted
            , when the connection to the irc-server was made
        """
        self.logger.info('made connection to ' + self.transport.addr[0])
        irc.IRCClient.connectionMade(self)
        self._apirunner('connectionMade')

    def connectionLost(self, reason):
        """ this is called by twisted,
            if the connection to the IRC-Server was lost
            @type reason:    twisted.python.failure.Failure
        """
        self.logger.info('lost connection: ' + str(reason))
        irc.IRCClient.connectionLost(self)
        self._apirunner('connectionLost', {'reason': reason})
        self.stopPlugins()

    def signedOn(self):
        """ called by twisted,
            when we signed on the IRC-Server
        """
        self.logger.info('signed on ' + self.network + ' as ' + self.nickname)
        self._apirunner('signedOn')
        channelstojoin = self.channels
        self.channels = []
        for channel in channelstojoin:
            if self.config.getBool('enabled', False, 'main', self.network, channel):
                pw = self.config.get('password', '', 'main', self.network, channel)
                if pw:
                    self.join(unicode(channel).encode('iso-8859-1'), unicode(pw).encode('iso-8859-1'))
                else:
                    self.join(unicode(channel).encode('iso-8859-1'))

    def joined(self, channel):
        """ called by twisted,
            if we joined a channel
            @param channel: the channel we joined
            @type channel: string
        """
        channel = channel.lower()
        self.logger.info('joined ' + channel)
        self.channels.append(channel)
        self.channelmodes[channel] = {}
        self.sendLine('WHO %s' % channel)
        self.syncing_channels.append(channel)
        self.config.set('enabled', True, 'main', self.network, channel)

    @syncedChannel(argnum=0)
    def left(self, channel):
        """ called by twisted,
            if we left a channel
            @param channel: the channel we left
            @type channel: string
        """
        channel = channel.lower()
        self.logger.info('left ' + channel)
        self._apirunner('left', {'channel': channel})
        for user in self.user_list:
            if self.user_list[user].hasChannel(channel):
                self.user_list[user].removeChannel(channel)

        self.channels.remove(channel)
        self.config.set('enabled', False, 'main', self.network, channel)

    def isupport(self, options):
        for o in options:
            kv = o.split('=', 1)
            if len(kv) == 1:
                kv.append(True)
            self.serversupports[kv[0]] = kv[1]

        if 'PREFIX' in self.serversupports:
            (mode, sym) = self.serversupports['PREFIX'][1:].split(')')
            for i in range(0, len(mode)):
                self.modchars[1 ** i] = mode[i]
                self.modcharvals[i ** i] = sym[i]

            self.rev_modchars = dict([ (v, k) for (k, v) in self.modchars.iteritems() ])
            self.rev_modcharvals = dict([ (v, k) for (k, v) in self.modcharvals.iteritems() ])

    def toUnicode(self, str, network=None, channel=None):
        """
            convert a string to an unicode-object, trying to use the
            encoding given in config, with fallback to iso-8859-15
        """
        if channel and channel[0] not in self.supported.getFeature('CHANTYPES'):
            channel = None
        try:
            str = unicode(str, self.config.get('encoding', 'UTF-8', 'main', network=network, channel=channel))
        except UnicodeDecodeError:
            str = unicode(str, 'iso-8859-15', errors='replace')

        return str

    def resolveUser(self, user):
        """
            resolve a user hostmask (nick!user@host) to a userobject
            returns a known user, if its in the user_list. creates a new
            user_list entry, if possible. if only nick is known, it returns a
            incomplete user and does not store it in the user_list
        """
        assert type(user) == str or type(user) == unicode
        if user in self.user_list:
            return self.user_list[user]
        else:
            if '!' in user:
                nick = user.split('!')[0]
                user2 = self.getUserByNick(nick)
                if user2:
                    return user2
                parts = user.split('!')[1].split('@')
                newuser = IrcUser(nick, parts[0], parts[1], '', self.network)
                self.user_list[user] = newuser
                return newuser
            user2 = self.getUserByNick(user)
            if user2:
                return user2
            return IrcUser(user, user, '', '', self.network)

    def privmsg(self, user, channel, msg):
        """ called by twisted,
            if we received a message
            @param user: the user, which send the message
            @type user: string
            @param channel: the channel to which the message was sent or my
                            nickname if it was a private message
            @type channel: string
            @param msg: the message
            @type msg: string
        """
        channel = channel.lower()
        msg = self.toUnicode(msg, self.network, channel)
        user = self.resolveUser(user)
        char = msg[0]
        if char == self.config.get('commandChar', '!', 'main'):
            tmp = msg[1:].split(' ', 1)
            command = tmp[0]
            if len(tmp) == 2:
                options = tmp[1]
            else:
                options = ''
            self._synced_apirunner('command', {'user': user, 'channel': channel, 'command': command, 
               'options': options})
        if channel[0] not in self.supported.getFeature('CHANTYPES'):
            self._apirunner('query', {'user': user, 'channel': channel, 
               'msg': msg})
        else:
            self._synced_apirunner('msg', {'user': user, 'channel': channel, 'msg': msg})

    @syncedAll
    def irc_unknown(self, prefix, command, params):
        """ called by twisted
            for every line that has no own callback
        """
        self._apirunner('irc_unknown', {'prefix': prefix, 'command': command, 'params': params})

    @syncedChannel(argnum=1)
    def noticed(self, user, channel, msg):
        """ called by twisted,
            if we got a notice
            @param user: the user which send the notice
            @type user: string
            @param channel: the channel to which the notice was sent (could be
                            our nick, if the message was only sent to us)
            @type channel: string
            @param msg: the message
            @type msg: string
        """
        channel = channel.lower()
        user = self.resolveUser(user)
        msg = self.toUnicode(msg, self.network, channel)
        self._apirunner('noticed', {'user': user, 'channel': channel, 
           'msg': msg})

    @syncedChannel(argnum=1)
    def action(self, user, channel, msg):
        """ called by twisted,
            if we received a action
            @param user: the user which send the action
            @type user: string
            @param channel: the channel to which the action was sent (could be
                            our nick, if the message was only sent to us)
            @type channel: string
            @param msg: the message
            @type msg: string
        """
        channel = channel.lower()
        user = self.resolveUser(user)
        msg = self.toUnicode(msg, self.network, channel)
        self._apirunner('action', {'user': user, 'channel': channel, 'msg': msg})

    @syncedChannel(argnum=1)
    def modeChanged(self, user, chan, set, modes, args):
        """ called by twisted
            if a usermode was changed
        """
        chan = chan.lower()
        user = self.resolveUser(user)
        if chan == self.nickname.lower():
            return
        mstr = 'mode change: user %s channel %s set %s modes %s args %s'
        if len(modes) != len(args):
            self.logger.debug('length of modes and args mismatched')
        elif user == chan:
            for i in range(0, len(modes)):
                if set:
                    self.mymodes[modes[i]] = args[i]
                else:
                    del self.mymodes[modes[i]]

        else:
            for i in range(0, len(modes)):
                if modes[i] in MODE_CHARS:
                    u = self.getUserByNick(args[i])
                    if u:
                        if chan in u.getChannels():
                            if set:
                                u.setMode(chan, modes[i])
                            else:
                                u.removeMode(chan, modes[i])
                        else:
                            self.logger.warning('user %s is not in channel %s' % (u.getHostMask(), chan))
                    else:
                        self.logger.error(args[i] + ' not known to me')
                else:
                    am = self.supported.getFeature('CHANMODES')['addressModes']
                    if modes[i] in am:
                        if set:
                            if modes[i] not in self.channelmodes[chan]:
                                self.channelmodes[chan][modes[i]] = []
                            self.channelmodes[chan][modes[i]].append(args[i])
                        elif modes[i] in self.channelmodes[chan] and args[i] in self.channelmodes[chan][modes[i]]:
                            self.channelmodes[chan][modes[i]].remove(args[i])
                    elif set:
                        self.channelmodes[chan][modes[i]] = args[i]
                    else:
                        del self.channelmodes[chan][modes[i]]

            self._apirunner('modeChanged', {'user': user, 'channel': chan, 'set': set, 
               'modes': modes, 'args': [ str(arg) for arg in args ]})

    @syncedChannel(argnum=0)
    def kickedFrom(self, channel, kicker, message):
        """ called by twisted,
            if the bot was kicked
        """
        message = self.toUnicode(message, self.network)
        channel = channel.lower()
        self.logger.info('I was kicked from ' + channel + ' by ' + kicker)
        self._apirunner('kickedFrom', {'channel': channel, 'kicker': kicker, 'message': message})
        self.channels.remove(channel)
        self.config.set('enabled', False, 'main', self.network, channel)
        for user in self.user_list:
            if self.user_list[user].hasChannel(channel):
                self.user_list[user].removeChannel(channel)

    @syncedChannel(argnum=1)
    def userKicked(self, kickee, channel, kicker, message):
        """ called by twisted,
            if a user was kicked
        """
        message = self.toUnicode(message, self.network)
        channel = channel.lower()
        self._apirunner('userKicked', {'kickee': kickee, 'channel': channel, 'kicker': kicker, 
           'message': message})
        user = self.getUserByNick(kickee).removeChannel(channel)

    @syncedChannel(argnum=1)
    def userJoined(self, user, channel):
        """ called by twisted,
            if a C{user} joined the C{channel}
        """
        channel = channel.lower()
        user = self.resolveUser(user)
        user.addChannel(channel)
        self._apirunner('userJoined', {'user': user, 'channel': channel})

    @syncedChannel(argnum=1)
    def userLeft(self, user, channel):
        """ called by twisted,
            if a C{user} left the C{channel}
        """
        channel = channel.lower()
        user = self.resolveUser(user)
        nick = user.getNick()
        self._apirunner('userLeft', {'user': user, 'channel': channel})
        user.removeChannel(channel)

    @syncedAll
    def userQuit(self, user, quitMessage):
        """ called by twisted,
            if a C{user} quits
        """
        quitMessage = self.toUnicode(quitMessage, self.network)
        user = self.resolveUser(user)
        nick = user.getNick()
        self._apirunner('userQuit', {'user': user, 'quitMessage': quitMessage})
        if user.getHostMask() in self.user_list:
            del self.user_list[user.getHostMask()]
        elif user.getNick().lower() in self.user_list:
            del self.user_list[user.getNick().lower()]
        else:
            self.logger.debug('user with nick %s quit, but was not in user_list' % nick)

    def yourHost(self, info):
        """ called by twisted
            with information about the IRC-Server we are connected to
        """
        self._apirunner('yourHost', {'info': info})

    @syncedChannel(argnum=1)
    def ctcpUnknownQuery(self, user, channel, messages):
        """ called by twisted,
            if a C{user} sent a ctcp query
        """
        channel = channel.lower()
        user = self.resolveUser(user)
        self._apirunner('ctcpQuery', {'user': user, 'channel': channel, 'messages': messages})

    @syncedChannel(argnum=1)
    def ctcpUnknownReply(self, user, channel, tag, data):
        """ called by twisted,
            if a C{user} sent a ctcp reply
        """
        channel = channel.lower()
        user = self.resolveUser(user)
        self._apirunner('ctcpReply', {'user': user, 'channel': channel, 'tag': tag, 
           'data': data})

    @syncedAll
    def userRenamed(self, oldname, newname):
        """ called by twisted,
            if a user changed his nick
        """
        self._apirunner('userRenamed', {'oldname': oldname, 'newname': newname})
        user = self.getUserByNick(oldname)
        if user and user.getHostMask() in self.user_list:
            del self.user_list[user.getHostMask()]
        else:
            self.logger.warning('%s not found in user_list!' % user.getHostMask())
        user.setNick(newname)
        self.user_list[user.getHostMask()] = user

    @syncedChannel(argnum=1)
    def topicUpdated(self, user, channel, newTopic):
        """ called by twisted
            if the topic was updated
        """
        channel = channel.lower()
        newTopic = self.toUnicode(newTopic, self.network, channel)
        self._apirunner('topicUpdated', {'user': user, 'channel': channel, 
           'newTopic': newTopic})

    def irc_RPL_WHOREPLY(self, prefix, params):
        """
            "<channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real name>"
        """
        (t, channel, user, host, server, nick, modes, hopsrealname) = params
        channel = channel.lower()
        (hops, realname) = hopsrealname.split(' ', 1)
        mask = '%s!%s@%s' % (nick, user, host)
        if mask in self.user_list:
            self.user_list[mask].realname = realname
        else:
            u = IrcUser(nick, user, host, realname, self)
            self.user_list[mask] = u
        if modes[(-1)] in MODE_CHARS:
            s = modes[(-1)]
        else:
            s = ' '
        self.user_list[mask].addChannel(channel)
        self.user_list[mask].setMode(channel, s)
        self._apirunner('irc_RPL_WHOREPLY', {'channel': channel, 'user': mask, 'server': server, 'realname': realname})

    def irc_RPL_ENDOFWHO(self, prefix, params):
        """
            end of WHO replies by the server
        """
        (nickname, channel, message) = params
        if channel in self.syncing_channels:
            self.logger.debug('ENDOFWHO(%s) - %s callbacks possibly waiting' % (channel, len(self.callback_queue)))
            self.sync_lock.acquire()
            self.syncing_channels.remove(channel)
            execute_now = []
            for callback in self.callback_queue:
                (channels, (func, args, kwargs)) = callback
                if len(set(channels).intersection(set(self.syncing_channels))) == 0:
                    execute_now.append(callback)

            count = len(execute_now)
            for callback in execute_now:
                (channels, (func, args, kwargs)) = callback
                try:
                    func(self, *args, **kwargs)
                except Exception, e:
                    self.logerror(self.logger, func.__name__, e)

            self.sync_lock.release()
            for callback in execute_now:
                self.callback_queue.remove(callback)

            self.logger.debug('ENDOFWHO(%s) - %s waiting callbacks executed' % (channel, count))
            self._apirunner('joined', {'channel': channel})
        self._apirunner('irc_RPL_ENDOFWHO', {'channel': channel})

    @syncedChannelRaw
    def irc_INVITE(self, prefix, params):
        """ called by twisted,
            if the bot was invited
        """
        channel = params[(-1)].lower()
        self._apirunner('invitedTo', {'channel': channel, 'inviter': prefix})

    def irc_RPL_BOUNCE(self, prefix, params):
        """ Overridden to get isupport work correctly """
        self.isupport(params[1:-1])

    def irc_JOIN(self, prefix, params):
        """ Overridden to get the full hostmask """
        nick = string.split(prefix, '!')[0]
        channel = params[(-1)]
        if nick.lower() == self.nickname.lower():
            self.hostmask = prefix
            self.joined(channel)
        else:
            self.userJoined(prefix, channel)

    def irc_PART(self, prefix, params):
        """ Overridden to get the full hostmask """
        nick = string.split(prefix, '!')[0]
        channel = params[0]
        if nick.lower() == self.nickname.lower():
            self.left(channel)
        else:
            self.userLeft(prefix, channel)

    def irc_QUIT(self, prefix, params):
        """ Overridden to get the full hostmask """
        self.userQuit(prefix, params[0])

    def lineReceived(self, line):
        """ called by twisted
            for every line which was received from the IRC-Server
        """
        self._apirunner('lineReceived', {'line': line})
        irc.IRCClient.lineReceived(self, line)

    def sendLine(self, line):
        self.lastLine = time.time()
        self._apirunner('sendLine', {'line': line})
        irc.IRCClient.sendLine(self, line)

    def ping(self):
        self.sendLine('PING %f' % time.time())

    def disconnect(self):
        """
            disconnects cleanly from the current network
        """
        self._apirunner('stop')
        self.factory.allow_disconnect()
        self.quit('Bye')