# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/get_url.py
# Compiled at: 2020-04-19 19:55:58
from dez.http.client import HTTPClient
import event

def main(**kwargs):
    url = 'http://%s:%s/' % (kwargs['domain'], kwargs['port'])
    c = HTTPClient()
    c.get_url(url, cb=req_cb, timeout=1)
    event.signal(2, event.abort)
    event.dispatch()


def req_cb(response):
    print response.status_line