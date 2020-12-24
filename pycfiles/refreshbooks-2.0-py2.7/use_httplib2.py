# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/refreshbooks/transports/use_httplib2.py
# Compiled at: 2014-01-17 12:08:47
import httplib2
from refreshbooks import exceptions as exc

class Transport(object):

    def __init__(self, url, headers_factory):
        self.client = httplib2.Http()
        self.url = url
        self.headers_factory = headers_factory

    def __call__(self, entity):
        resp, content = self.client.request(self.url, 'POST', headers=self.headers_factory(), body=entity)
        if resp.status >= 400:
            raise exc.TransportException(resp.status, content)
        return content