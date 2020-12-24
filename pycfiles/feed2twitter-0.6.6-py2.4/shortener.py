# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/feed2twitter/shortener.py
# Compiled at: 2009-08-19 14:33:15
import urllib
from xml.dom.minidom import parseString

class TinyURL(object):
    __module__ = __name__

    def short(self, url):
        try:
            params = urllib.urlencode({'url': url})
            fp = urllib.urlopen('http://tinyurl.com/api-create.php', params)
            return fp.read()
        except IOError, e:
            raise 'urllib error.'


class IsGD(object):
    __module__ = __name__

    def short(self, url):
        try:
            params = urllib.urlencode({'longurl': url})
            url = 'http://is.gd/api.php?%s' % params
            fp = urllib.urlopen(url)
            return fp.read()
        except IOError, e:
            raise 'urllib error.'


class MigreME(object):
    __module__ = __name__

    def short(self, url):
        try:
            params = urllib.urlencode({'url': url})
            url = 'http://migre.me/api.xml?%s' % params
            fp = urllib.urlopen(url)
            dom = parseString(fp.read())
            return dom.getElementsByTagName('migre')[0].childNodes[0].data
        except IOError, e:
            raise 'urllib error.'


services = {'tinyurl': TinyURL, 'is.gd': IsGD, 'migre.me': MigreME}