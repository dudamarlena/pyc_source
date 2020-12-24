# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/clickatell/url.py
# Compiled at: 2010-05-21 03:18:27
import urllib, urllib2, logging
from clickatell.utils import Dispatcher

class URLDispatcher(Dispatcher):

    def do_post(self, url, data, headers):
        params = urllib.urlencode(data)
        request = urllib2.Request(url, data, headers)
        logging.debug('POST %s with %s' % (url, data))
        return (request, urllib2.urlopen(request))

    def do_get(self, url, data, headers):
        params = urllib.urlencode(data)
        full_url = '%s?%s' % (url, params)
        logging.debug('GET %s' % full_url)
        request = urllib2.Request(full_url, None, headers)
        return (request, urllib2.urlopen(request))


url_dispatcher = URLDispatcher()

def open(method, url, data={}, headers={}):
    return url_dispatcher.dispatch(method, url, data, headers)