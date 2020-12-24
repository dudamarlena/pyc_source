# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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