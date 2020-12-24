# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/ginsfsm/ginsfsm/examples/sockjs/test_sockjs_apps/pyramid_main.py
# Compiled at: 2013-04-22 15:23:27
"""
applic
======

TestApps

"""
from pyramid.security import Allow, Everyone, ALL_PERMISSIONS
from ginsfsm.gobj import GObj
from ginsfsm.c_timer import GTimer
from ginsfsm.protocols.sockjs.server.c_sockjs_server import GSockjsServer
from .test import EchoConnection, CloseConnection, CookieEcho
TESTAPPS_FSM = {}
TESTAPPS_GCONFIG = {}

class TestSocksjsApps(GObj):
    """  Root resource for TestApps.

    .. ginsfsm::
       :fsm: TESTAPPS_FSM
       :gconfig: TESTAPPS_GCONFIG

    *Input-Events:*
        * :attr:`'EV_TIMEOUT'`: Timer over.

    """
    __acl__ = [
     (
      Allow, Everyone, ALL_PERMISSIONS)]

    def __init__(self):
        GObj.__init__(self, TESTAPPS_FSM, TESTAPPS_GCONFIG)

    def start_up(self):
        """ Initialization zone.
        """
        self.timer = self.create_gobj(None, GTimer, self)
        self.echo = self.create_gobj('echo', GSockjsServer, self, sockjs_app_class=EchoConnection, response_limit=4096)
        self.disabled_websocket_echo = self.create_gobj('disabled_websocket_echo', GSockjsServer, self, sockjs_app_class=EchoConnection, disabled_transports=[
         'websocket'])
        self.disabled_websocket_echo = self.create_gobj('close', GSockjsServer, self, sockjs_app_class=CloseConnection)
        self.disabled_websocket_echo = self.create_gobj('cookie_needed_echo', GSockjsServer, self, sockjs_app_class=CookieEcho)
        return