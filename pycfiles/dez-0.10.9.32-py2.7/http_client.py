# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/http_client.py
# Compiled at: 2020-04-19 19:55:58
from dez.http.client import HTTPClientRequest, HTTPClient
import event

def main(**kwargs):
    client = HTTPClient()
    client.get_connection(kwargs['domain'], kwargs['port'], get_conn_cb, [])
    event.dispatch()


def get_conn_cb(conn):
    print (
     'GOT conn', conn)
    req = HTTPClientRequest(conn)
    req.dispatch(response_headers_end_cb, [])


def response_headers_end_cb(response):
    response.read_body(response_completed_cb, [response])


def alternate_response_headers_end_cb(response):
    print 'woot4'
    response.read_body_stream(response_body_stream_cb, [response])


def response_body_stream_cb(chunk, response):
    print chunk


def response_completed_cb(body, response):
    print 'woot5'
    print response.status_line
    print response.headers
    print '#########'
    print ('body len:', len(body))
    event.abort()