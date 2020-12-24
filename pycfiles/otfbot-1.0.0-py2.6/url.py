# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/url.py
# Compiled at: 2011-04-22 06:35:42
import urllib2, re, string
from HTMLParser import HTMLParser, HTMLParseError
from otfbot.lib import chatMod, urlutils
from otfbot.lib.pluginSupport.decorators import callback

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.parser = titleExtractor()
        self.autoTiny = self.bot.config.get('autotiny', False, 'url', self.bot.network)
        self.autoTinyLength = int(self.bot.config.get('autoLength', '50', 'url', self.bot.network))
        self.autoPreview = self.bot.config.get('autopreview', False, 'url', self.bot.network)
        self.lasturl = ''

    @callback
    def command(self, user, channel, command, options):
        response = ''
        self.parser = titleExtractor()
        headers = None
        if 'preview' in command:
            if options == '':
                if self.lasturl:
                    options = self.lasturl
                else:
                    return
            d = urlutils.get_headers(options)
            d.addCallback(self.checkForHTML, options, channel)
            d.addErrback(self.error, channel)
        if 'tinyurl' in command:
            if options == '':
                options = self.lasturl
            d = urlutils.download('http://tinyurl.com/api-create.php?url=' + options)
            d.addCallback(self.processTiny, channel)
            d.addErrback(self.error, channel)
        return

    def error(self, failure, channel):
        self.bot.sendmsg(channel, 'Error while retrieving informations: ' + failure.getErrorMessage())

    def processTiny(self, data, channel):
        self.bot.sendmsg(channel, '[Link Info] ' + data)

    def checkForHTML(self, header, url, channel):
        if urlutils.is_html(header):
            d = urlutils.download(url, headers={'Accept': 'text/html'})
            d.addCallback(self.processPreview, channel)
            d.addErrback(self.error, channel)
        else:
            info = ''
            if 'content-type' in header:
                info += 'Mime-Type: %s' % header['content-type']
            if 'content-length' in header:
                size = urlutils.convert_bytes(header['content-length'])
                info += ', %s' % size
            self.bot.sendmsg(channel, '[Link Info] ' + info)

    def processPreview(self, data, channel):
        try:
            self.parser.feed(data)
            if self.parser.get_result() != '':
                self.bot.sendmsg(channel, '[Link Info] ' + self.parser.get_result())
        except HTMLParseError, e:
            self.logger.debug(e)
            del self.parser
            self.parser = titleExtractor()

        self.parser.reset()

    @callback
    def msg(self, user, channel, msg):
        mask = 0
        regex = re.match('.*((ftp|http|https):(([A-Za-z0-9$_.+!*(),;/?:@&~=-])|%[A-Fa-f0-9]{2}){2,}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*(),;/?:@&~=%-]*))?([A-Za-z0-9$_+!*();/?:~-])).*', msg)
        if regex:
            url = regex.group(1)
            if string.lower(user.getNick()) != string.lower(self.bot.nickname):
                cmd = ''
                if 'tinyurl.com' not in url:
                    if len(url) > self.autoTinyLength and self.autoTiny:
                        cmd += '+tinyurl'
                    else:
                        self.lasturl = url
                if self.autoPreview:
                    cmd += '+preview'
                self.command(user, channel, cmd, url)


class titleExtractor(HTMLParser):
    intitle = False
    title = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.intitle = True
        else:
            self.intitle = False

    def handle_endtag(self, tag):
        if tag == 'title':
            self.intitle = False

    def handle_data(self, data):
        if self.intitle:
            self.title = data

    def get_result(self):
        title = self.title.replace('\n', ' ').replace('\r', '')
        title = re.sub('[ ]+', ' ', title)
        return title