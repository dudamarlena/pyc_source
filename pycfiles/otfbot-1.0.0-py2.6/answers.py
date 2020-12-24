# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/answers.py
# Compiled at: 2011-04-22 06:35:42
"""
    Send answers from file based on regexes
"""
import string, re
from otfbot.lib import chatMod
from otfbot.lib import functions
from otfbot.lib.pluginSupport.decorators import callback

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot

    def start(self):
        self.answersFile = self.bot.config.getPath('file', datadir, 'answers.txt', 'answer')
        self.encoding = self.bot.config.get('fileencoding', 'iso-8859-15', 'answer')
        self.reload()

    @callback
    def action(self, user, channel, msg):
        return self.msg(user, channel, msg)

    @callback
    def msg(self, user, channel, msg):
        user = user.getNick()
        if channel in self.bot.channels:
            answer = self.respond(user, msg)
            if answer != '':
                self.bot.sendmsg(channel, answer, self.encoding)

    def reload(self):
        """
            load the answers from the configured file
        """
        self.answers = functions.loadProperties(self.answersFile)

    def respond(self, user, msg):
        """
            assemble a response

            @param user: name of the user which issued the message
            @param msg: the message which needs a response
        """
        answer = ''
        for key in self.answers.keys():
            if re.search(key, msg, re.I):
                answer = self.answers[key]
                answer = re.sub('USER', user, answer)
                answer = re.sub('MESSAGE', msg, answer)

        if len(answer) > 0 and answer[(-1)] == '\n':
            return answer[0:-1]
        else:
            return answer