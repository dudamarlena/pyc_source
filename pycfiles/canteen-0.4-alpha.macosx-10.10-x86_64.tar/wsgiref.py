# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/runtime/wsgiref.py
# Compiled at: 2014-09-26 04:50:19
"""

  stdlib runtime
  ~~~~~~~~~~~~~~

  runs :py:mod:`canteen`-based apps on python's stdlib library,
  :py:mod:`wsgiref`.

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
from ..core import runtime
with runtime.Library('wsgiref') as (library, wsgiref):
    simple_server = library.load('simple_server')

    class StandardWSGI(runtime.Runtime):
        """  """
        __default__ = True

        def bind(self, interface, port):
            """  """
            return simple_server.make_server(interface, port, self.dispatch)