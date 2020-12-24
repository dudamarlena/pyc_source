# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pypomelo/handler.py
# Compiled at: 2019-01-03 22:45:49
from __future__ import absolute_import, division, print_function, with_statement

class Handler(object):

    def on_connected(self, client, user_data):
        raise NotImplementedError()

    def on_recv_data(self, client, proto_type, data):
        return data

    def on_heartbeat(self, client):
        raise NotImplementedError()

    def on_response(self, client, route, request, response):
        raise NotImplementedError()

    def on_push(self, client, route, push_data):
        raise NotImplementedError()

    def on_disconnect(self, client):
        raise NotImplementedError()