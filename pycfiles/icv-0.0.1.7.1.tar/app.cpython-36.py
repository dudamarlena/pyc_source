# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/core/http/server/app.py
# Compiled at: 2019-05-11 08:37:20
# Size of source mod 2**32: 898 bytes
from icv.utils import is_seq, is_str
from ..methods import HttpMethod
from .simple_http_server import IcvServer
from .simple_http_handler import IcvHandler
from . import simple_http_handler

class App:

    def __init__(self, host='0.0.0.0', port=9527, app_name='Icv Http Server', debug=False):
        self._host = host
        self._port = port
        self._app_name = app_name
        self._debug = debug
        self._server = IcvServer(host, port)
        simple_http_handler._init_routes()

    def route(self, action, methods=HttpMethod.methods):
        if not is_seq(methods):
            if not is_str(methods):
                raise AssertionError

        def decorate(function):
            simple_http_handler.add_route(action, methods, function)

        return decorate

    def start(self):
        print('>>>>>>> server now running at {}:{} <<<<<<<'.format(self._host, self._port))
        self._server.run(IcvHandler)