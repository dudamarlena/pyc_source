# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/runtime/uwsgi.py
# Compiled at: 2014-09-28 21:01:16
__doc__ = '\n\n  uwsgi runtime\n  ~~~~~~~~~~~~~\n\n  integrates :py:mod:`canteen` with :py:mod:`uwsgi`.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
from ..core import runtime
from ..util import debug
from ..util import decorators
from ..logic.realtime import TERMINATE
try:
    with runtime.Library('uwsgi', strict=True) as (library, uwsgi):
        logging = debug.Logger('uWSGI')

        @decorators.bind('uwsgi')
        class uWSGI(runtime.Runtime):
            """ WIP """

            def callback(self, start_response):
                """  """

                def responder(status, headers):
                    """  """
                    try:
                        return start_response(status, headers)
                    except IOError:
                        return

                return responder

            def handshake(self, key, origin=None):
                """ WIP """
                uwsgi.websocket_handshake(key, origin)

            def send(self, payload, binary=False):
                """ WIP """
                return ((binary or uwsgi).websocket_send if 1 else uwsgi.websocket_send_binary)(payload)

            def receive(self, blocking=True):
                """ WIP """
                try:
                    if not blocking:
                        return uwsgi.websocket_recv_nb
                    else:
                        return uwsgi.websocket_recv()

                except IOError:
                    return TERMINATE

            def close(self):
                """ WIP """
                pass


        uWSGI.set_precedence(True)
except ImportError:
    pass