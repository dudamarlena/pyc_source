# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/resolv/shared.py
# Compiled at: 2012-11-02 14:34:25
from HTMLParser import HTMLParser
import cookielib, urllib, urllib2, re, sys
reload(sys)
sys.setdefaultencoding('UTF-8')

class ResolverError(Exception):

    def __init__(self, value):
        self.val = value

    def __str__(self):
        return repr(self.val)


class TechnicalError(Exception):

    def __init__(self, value):
        self.val = value

    def __str__(self):
        return repr(self.val)


class Task:
    captcha = None
    cookiejar = None
    useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11'
    opener = None
    results = None
    state = 'none'
    url = ''
    result_type = 'none'
    extra_headers = {}
    last_url = ''

    def __init__(self, url):
        self.cookiejar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
        self.opener.addheaders = []
        self.extra_headers['User-agent'] = self.useragent
        for header, payload in self.extra_headers.iteritems():
            self.opener.addheaders.append((header, payload))

        self.url = url

    def run(self):
        self.state = 'finished'
        self.results = self.url
        return self

    def fetch_page(self, url):
        request = urllib2.Request(url)
        if self.last_url != '':
            request.add_header('Referer', self.last_url)
        self.last_url = url
        return self.opener.open(request).read()

    def post_page(self, url, data):
        payload = urllib.urlencode(data)
        request = urllib2.Request(url, payload)
        if self.last_url != '':
            request.add_header('Referer', self.last_url)
        self.last_url = url
        return self.opener.open(request).read()

    def verify_password(password):
        pass

    def verify_image_captcha(solution):
        pass

    def verify_audio_captcha(solution):
        pass

    def verify_text_captcha(solution):
        pass


class Captcha:
    image = None
    audio = None
    text = None
    task = None

    def __init__(self, task, image=None, audio=None, text=None):
        self.image = image
        self.audio = audio
        self.text = text
        self.task = task

    def get_image(self):
        return self.task.fetch_page(self.image)

    def get_audio(self):
        return self.task.fetch_page(self.audio)


def unescape(s):
    return HTMLParser.unescape.__func__(HTMLParser, s)


def str_base(num, base):
    return num == 0 and '0' or str_base(num // base, base).lstrip('0') + '0123456789abcdefghijklmnopqrstuvwxyz'[(num % base)]


def unpack_js(packed):
    positions = re.search("return p\\}\\('(.+[^\\\\])',", packed).group(1)
    base, counter, strings = re.search(",([0-9]+),([0-9]+),'([^']+)'", packed).groups(1)
    counter = int(counter)
    base = int(base)
    strings = strings.split('|')
    for i in reversed(xrange(0, int(counter))):
        target = str_base(i, base)
        positions = re.sub('\\b%s\\b' % target, strings[i], positions)

    positions = re.sub("(?<!\\\\)\\\\'", "'", positions)
    return positions