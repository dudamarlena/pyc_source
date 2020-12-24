# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/youtube.py
# Compiled at: 2011-04-22 06:35:42
"""
search on youtube with !youtube search phrase
"""
from otfbot.lib import chatMod, urlutils
from otfbot.lib.pluginSupport.decorators import callback
import logging, urllib

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('youtube')
        self.feedparser = self.bot.depends_on_module('feedparser')

    def downloadFinished(self, content, channel):
        """
            callback for the download. parse the feedcontent and post
            the results to the channel given in channel

            @param content: xml-content of the search-feed
            @type content: str
            @param channel: the channel where the link should be posted
            @type channel: str
        """
        parsed = self.feedparser.parse(content)
        if len(parsed.entries):
            self.bot.sendmsg(channel, '%s - %s' % (parsed.entries[0]['link'].encode('UTF-8'), parsed.entries[0]['title'].encode('UTF-8')))
        else:
            self.bot.sendmsg(channel, 'Error: Nothing found')

    @callback
    def command(self, user, channel, command, options):
        if command == 'youtube' and options:
            urlutils.download('http://gdata.youtube.com/feeds/' + 'base/videos?q=%s&client=ytapi-youtube-search&alt=rss&v=2' % urllib.quote(options.encode('UTF-8'))).addCallback(self.downloadFinished, channel)