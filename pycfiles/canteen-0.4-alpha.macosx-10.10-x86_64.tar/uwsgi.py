# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/runtime/uwsgi.py
# Compiled at: 2014-09-28 21:01:16
"""

  uwsgi runtime
  ~~~~~~~~~~~~~

  integrates :py:mod:`canteen` with :py:mod:`uwsgi`.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
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