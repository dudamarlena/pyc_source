# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grs/gnews.py
# Compiled at: 2011-10-05 02:42:28
import urllib, urllib2, time, datetime
from datetime import timedelta
try:
    import simplejson as json
except:
    from django.utils import simplejson as json

class gnews(object):

    def __init__(self, q='', topic='', rsz=4):
        a = urllib2.urlopen('https://ajax.googleapis.com/ajax/services/search/news?%s&ned=tw&hl=zh-tw' % urllib.urlencode({'v': '1.0', 
           'q': q, 
           'rsz': rsz, 
           'topic': topic}))
        self.j = json.loads(a.read())
        self.formatre = {}
        l = 0
        for i in self.j['responseData']['results']:
            self.formatre.update({l: {'title': i['titleNoFormatting'], 'publisher': i['publisher'], 
                   'publisheddate': self.covdate(i['publishedDate']), 
                   'url': i['unescapedUrl']}})
            l += 1

    def p(self):
        print self.j['responseData']['cursor']['estimatedResultCount']
        for i in self.j['responseData']['results']:
            print i['titleNoFormatting']
            print i['content']
            print '----------'
            print i['publishedDate'], i['publisher']
            print i['unescapedUrl']
            print '==============='

    def x(self):
        rt = ''
        for i in self.formatre:
            rt += '\r\n%(title)s - %(publisher)s - %(publisheddate)s\r\n%(url)s' % self.formatre[i]

        return rt

    def covdate(self, timestring):
        time_format = '%a, %d %b %Y %H:%M:%S'
        a = datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestring[:-6], time_format)))
        return str(a + timedelta(hours=16))