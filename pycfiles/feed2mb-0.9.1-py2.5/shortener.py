# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/feed2mb/shortener.py
# Compiled at: 2010-09-01 16:07:39
import urllib
from xml.dom.minidom import parseString

class ShortenerException(Exception):
    pass


class TinyURL(object):

    def short(self, url):
        try:
            params = urllib.urlencode({'url': url})
            fp = urllib.urlopen('http://tinyurl.com/api-create.php', params)
            short_url = fp.read()
            if 'http' not in short_url:
                raise ShortenerException('tinyurl error')
            return short_url
        except IOError, e:
            raise ShortenerException('tinyurl error')


class MiudIn(object):

    def short(self, url):
        try:
            params = urllib.urlencode({'url': url})
            fp = urllib.urlopen('http://miud.in/api-create.php', params)
            short_url = fp.read()
            if 'http' not in short_url:
                raise ShortenerException('miud.in error')
            return short_url
        except IOError, e:
            raise ShortenerException('miud.in error')


class IsGD(object):

    def short(self, url):
        try:
            params = urllib.urlencode({'longurl': url})
            url = 'http://is.gd/api.php?%s' % params
            fp = urllib.urlopen(url)
            short_url = fp.read()
            if 'http' not in short_url:
                raise ShortenerException('tinyurl error')
            return short_url
        except IOError, e:
            raise ShortenerException('Is.gd error')


class MigreME(object):

    def short(self, url):
        try:
            params = urllib.urlencode({'url': url})
            url = 'http://migre.me/api.xml?%s' % params
            fp = urllib.urlopen(url)
            dom = parseString(fp.read())
            short_url = dom.getElementsByTagName('migre')[0].childNodes[0].data
            if 'http' not in short_url:
                raise ShortenerException('tinyurl error')
            return short_url
        except IOError, e:
            raise ShortenerException('migreme error')


services = {'tinyurl': TinyURL, 
   'is.gd': IsGD, 
   'migre.me': MigreME, 
   'miud.in': MiudIn}