# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/refreshbooks/transports/use_requests.py
# Compiled at: 2014-01-17 12:08:47
import requests
from refreshbooks import exceptions as exc

class Transport(object):

    def __init__(self, url, headers_factory):
        self.session = requests.session()
        self.url = url
        self.headers_factory = headers_factory

    def __call__(self, entity):
        resp = self.session.post(self.url, headers=self.headers_factory(), data=entity)
        if resp.status_code >= 400:
            raise exc.TransportException(resp.status_code, resp.content)
        return resp.content