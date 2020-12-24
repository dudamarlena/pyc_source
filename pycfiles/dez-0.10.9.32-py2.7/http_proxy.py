# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/http_proxy.py
# Compiled at: 2020-04-19 19:55:58
import time, event
from dez.network.client import SocketClient
from dez.http.client import HTTPClientRequest, HTTPClient
from dez.http.server import HTTPDaemon, HTTPResponse, RawHTTPResponse
from dez.http.client.response import HTTPClientReader
client = SocketClient()

def proxy(request):
    client.get_connection('www.orbited.org', 80, connection_cb, [request])


def connection_cb(conn, request):
    conn.write(request.action + '\r\n')
    for key, val in list(request.headers.items()):
        conn.write('%s: %s\r\n' % (key, val))

    conn.write('\r\n')
    request.read_body_stream(body_cb, [conn, request])


def body_cb(data, conn, request):
    if not data:
        reader = HTTPClientReader(conn)
        reader.get_headers_only(response_headers_cb, [reader, request])
    else:
        conn.write(data)


def response_headers_cb(response, reader, request):
    request.write(response.status_line + '\r\n')
    for key, val in list(response.case_match_headers.items()):
        request.write('%s: %s\r\n' % (val, response.headers[key]))

    request.write('\r\n')
    reader.get_body_stream(response_body_cb, [request])


def response_body_cb(response, size, request):
    if size == 0:
        print 'request.end'
        return request.end()
    request.write(response.body.get_value())
    response.body.reset()


def main(**kwargs):
    event.signal(2, event.abort)
    server = HTTPDaemon('', kwargs['port'])
    server.register_prefix('/', proxy)
    event.dispatch()