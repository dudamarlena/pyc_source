# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/http_client2.py
# Compiled at: 2020-04-19 19:55:58
from dez.http.client import HTTPClientRequest, HTTPClient
import event, time

def main(**kwargs):
    event.initialize(['pyevent'])
    client = HTTPClient()
    for i in range(20):
        client.get_url('http://' + domain + ':' + port + '/', cb=response_cb, cbargs=[i + 1])

    event.signal(2, event.abort)
    event.dispatch()


def response_cb(response, i):
    print (
     i, time.time(), response.status_line)