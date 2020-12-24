# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googl/__init__.py
# Compiled at: 2011-04-04 16:03:13
import httplib2, urllib
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise ImportError('You need to have a json parser, easy_install simplejson')

class Googl:
    """Access Goo.gl url shorten"""

    def __init__(self, key=None, baseurl='https://www.googleapis.com/urlshortener/v1/url', user_agent='python-googl'):
        self.key = key
        self.conn = httplib2.Http()
        self.baseurl = baseurl
        self.user_agent = user_agent

    def _request(self, url='', method='GET', body='', headers=None, userip=None):
        """send request and parse the json returned"""
        if not url:
            url = self.baseurl
        elif not url.startswith('http'):
            url = '%s?%s' % (self.baseurl, url)
        if self.key is not None:
            url += '%s%s' % ('?' if '?' not in url else '&', 'key=%s' % self.key)
        if userip:
            url += '%s%s' % ('?' if '?' not in url else '&', 'userip=%s' % userip)
        if headers is None:
            headers = {}
        if 'user-agent' not in headers:
            headers['user-agent'] = self.user_agent
        return json.loads(self.conn.request(url, method, body=body, headers=headers)[1])

    def shorten(self, url, userip=None):
        """shorten the url"""
        body = json.dumps(dict(longUrl=url))
        headers = {'content-type': 'application/json'}
        return self._request(method='POST', body=body, headers=headers, userip=userip)

    def expand(self, url, analytics=False, userip=None):
        """expand the url"""
        data = dict(shortUrl=url)
        if analytics:
            data['projection'] = 'FULL'
        if userip:
            data['userip'] = userip
        url = urllib.urlencode(data)
        return self._request(url)