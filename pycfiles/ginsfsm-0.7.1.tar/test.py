# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/ginsfsm/ginsfsm/examples/sockjs/test_sockjs_apps/test.py
# Compiled at: 2013-04-22 15:23:27
""" SockJSConnection GObj

.. autoclass:: SockJSConnection
    :members: start_up

"""
import math
from ginsfsm.protocols.sockjs.server.conn import SockJSConnection

class EchoConnection(SockJSConnection):

    def on_message(self, msg):
        self.send(msg)


class CloseConnection(SockJSConnection):

    def on_open(self, info):
        self.close()

    def on_message(self, msg):
        pass


class CookieEcho(SockJSConnection):

    def on_message(self, msg):
        self.send(msg)