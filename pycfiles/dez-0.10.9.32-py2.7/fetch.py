# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/http/fetch.py
# Compiled at: 2018-06-10 07:17:26
from dez.json import decode
from dez.logging import get_logger_getter
from dez.http.client import HTTPClient
F = None

class Fetcher(HTTPClient):

    def __init__(self):
        HTTPClient.__init__(self)
        self.log = get_logger_getter('dez')('Fetcher').simple

    def fetch(self, host, path='/', port=80, cb=None, timeout=1):
        url = 'http://%s:%s%s' % (host, port, path)
        self.log('fetching: %s' % (url,))
        HTTPClient().get_url(url, cb=lambda resp: (cb and cb or self.log)(resp.body), timeout=timeout)


def fetch(host, path='/', port=80, cb=None, timeout=1, json=False, dispatch=False):
    global F
    if not F:
        F = Fetcher()
    if json:
        cb = lambda data: cb(decode(data))
    F.fetch(host, path, port, cb, timeout)
    if dispatch:
        import event
        event.signal(2, event.abort)
        event.dispatch()