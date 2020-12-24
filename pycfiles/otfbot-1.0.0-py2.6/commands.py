# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/commands.py
# Compiled at: 2011-04-22 06:35:42
"""
React to !commands with text from a commands.txt file
"""
from otfbot.lib import chatMod
from otfbot.lib import functions
from otfbot.lib.pluginSupport.decorators import callback
import string, re, random, os

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.channels = []
        self.mtime = 0

    @callback
    def connectionMade(self):
        self.start()

    @callback
    def joined(self, channel):
        filename = self.bot.config.getPath('file', datadir, 'commands.txt', 'commands', self.bot.network, channel)
        enc = self.bot.config.get('fileencoding', 'iso-8859-15', 'commands', self.bot.network, channel)
        self.commands[channel] = functions.loadProperties(filename, True, enc)

    @callback
    def command(self, user, channel, command, options):
        user = user.getNick()
        if self.bot.config.getBool('autoReload', True, 'commands', self.bot.network, channel):
            net_file = self.bot.config.getPath('file', datadir, 'commands.txt', 'commands', self.bot.network)
            network_mtime = os.stat(net_file).st_mtime
            global_file = self.bot.config.getPath('file', datadir, 'commands.txt', 'commands')
            general_mtime = os.stat(global_file).st_mtime
            if self.mtime < network_mtime or self.mtime < general_mtime:
                self.reload()
                self.mtime = max(network_mtime, general_mtime)
        if user != self.bot.nickname:
            answer = self.respond(channel, user, command.lower(), options)
            if answer != '':
                if answer[0] == ':':
                    self.bot.sendmsg(channel, answer[1:])
                else:
                    self.bot.sendme(channel, answer)

    def start(self):
        self.register_ctl_command(self.reload)
        self.commands = {}
        enc = self.bot.config.get('fileencoding', 'iso-8859-15', 'commands')
        file = self.bot.config.getPath('file', datadir, 'commands.txt', 'commands')
        self.commands['general'] = functions.loadProperties(file, True, enc)
        enc = self.bot.config.get('fileencoding', 'iso-8859-15', 'commands', self.bot.network)
        file = self.bot.config.getPath('file', datadir, 'commands.txt', 'commands', self.bot.network)
        self.commands['network'] = functions.loadProperties(file, True, enc)
        for chan in self.bot.channels:
            self.joined(chan)

    def reload(self):
        self.start()
        return 'reloaded commands'

    def getCommand(self, channel, cmd):
        if channel not in self.commands:
            self.commands[channel] = {}
        if channel in self.commands and cmd in self.commands[channel]:
            return self.commands[channel][cmd]
        else:
            if 'network' in self.commands and cmd in self.commands['network']:
                return self.commands['network'][cmd]
            if 'general' in self.commands and cmd in self.commands['general']:
                return self.commands['general'][cmd]
            return ''

    def respond(self, channel, user, command, options):
        """
        respond to a command, substituting USER by the actual user
        and OTHER by the given options

        >>> c=Plugin(None)
        >>> c.commands={} #just for the example to work
        >>> c.commands['general']={"test": ["USER wanted a test"],
        >>> "test_": ["USER wanted to show OTHER how it works"]}
        >>> c.commands['network']={}
        >>> #example begins here:
        >>> c.respond("", "testuser", "test", "")
        'testuser wanted a test'
        >>> c.respond("", "testuser", "test", "you")
        'testuser wanted to show you how it works'
        """
        answer = ''
        if len(options) >= 1:
            options = options.rstrip()
            answers = self.getCommand(channel, command + '_')
            if len(answers):
                answer = random.choice(answers)
                answer = re.sub('OTHER', options, answer)
        else:
            answers = self.getCommand(channel, command)
            if len(answers):
                answer = random.choice(answers)
        answer = re.sub('USER', user, answer)
        if len(answer) > 0 and answer[(-1)] == '\n':
            return answer[0:-1]
        else:
            return answer