# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/refreshbooks/transports/use_urllib2.py
# Compiled at: 2014-01-20 11:54:38
import sys
if sys.version_info.major == 3:
    import urllib.request as u
else:
    import urllib2 as u
from refreshbooks import exceptions as exc

class Transport(object):

    def __init__(self, url, headers_factory):
        self.url = url
        self.headers_factory = headers_factory

    def __call__(self, entity):
        request = u.Request(url=self.url, data=entity, headers=self.headers_factory())
        try:
            return u.urlopen(request).read()
        except u.HTTPError as e:
            raise exc.TransportException(e.code, e.read())