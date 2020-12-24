# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyupnptools/http_request.py
# Compiled at: 2018-09-02 06:52:47
from .upnp import *
import requests, logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class HttpRequest(UPnPRequest):

    def __init__(self, url):
        self._url = url

    def request(self, method='GET', *args, **kwargs):
        try:
            res = getattr(requests, method.lower())(self._url, *args, **kwargs)
        except AttributeError:
            res = requests.request(method.lower(), self._url, *args, **kwargs)

        logger.debug(('http response / status code: {}').format(res.status_code))
        ret = UPnPResponse()
        for k in res.headers.keys():
            ret.header(k, res.headers[k])

        ret.data(res.text.encode('utf-8'))
        return ret