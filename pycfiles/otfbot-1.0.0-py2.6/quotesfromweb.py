# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/quotesfromweb.py
# Compiled at: 2011-04-22 06:35:42
"""
    Sends quotes and proverbs to the channel
"""
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback
import urllib2, re

class Plugin(chatMod.chatMod):
    """ quotesfromweb plugin """
    quoteurl = 'http://www.all4quotes.com/quote/rss/quotes/'

    def __init__(self, bot):
        self.bot = bot
        self.feedparser = self.bot.depends_on_module('feedparser')

    @callback
    def command(self, user, channel, command, options):
        """
            Handels the commands !zitat, !sprichwort and !proverb and posts appropriate phrases in the channel
        """
        if command.lower() == 'zitat':
            zitat = self.feedparser.parse(self.quoteurl)
            zitat = zitat['entries'][0]
            desc = zitat['description'].replace('<p class="q_pate"><a href="http://www.all4quotes.com/paten-information/b3967a0e938dc2a6340e258630febd5a/" target="_blank" title="Treffsichere Textlinkwerbung">Werden Sie Zitatepate&trade;</a></p>', '').encode('utf8')
            desc = desc.replace(re.findall('<p.*class=".+">.+</p>', desc)[0], '')
            self.bot.msg(channel, '"' + desc + '" (' + zitat['title'].encode('utf8') + ')')
            return
        if command == 'sprichwort':
            url = urllib2.urlopen('http://www.sprichwortrekombinator.de')
        elif command == 'proverb':
            url = urllib2.urlopen('http://proverb.gener.at/or/')
        else:
            return
        data = url.read()
        url.close()
        sprichwort = re.search('<div class="spwort">([^<]*)<\\/div>', data, re.S).group(1)
        self.bot.sendmsg(channel, sprichwort)