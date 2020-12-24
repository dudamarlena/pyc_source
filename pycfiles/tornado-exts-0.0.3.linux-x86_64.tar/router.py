# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tornado_extensions/sockjs/router.py
# Compiled at: 2013-09-03 05:36:04
import sockjs.tornado
from .mixins import BroadcastMixin

class CustomSockJSRouter(sockjs.tornado.SockJSRouter, BroadcastMixin):
    """Router is a Comet server that serves client sockets.

    Extended summary
    ----------------
    This router extends the base class `sockjs.tornado.SockJSRouter` and
    includes `BroadcastMixin`.
    """
    pass