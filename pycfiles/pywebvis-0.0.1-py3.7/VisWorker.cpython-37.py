# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webvis/VisWorker.py
# Compiled at: 2019-11-05 21:15:15
# Size of source mod 2**32: 1951 bytes
import webbrowser, json
from . import helpers
from . import interface as ifc
from .helpers import threaded
from .ws_server import start_server as serve_ws
from .ws_server import stop as stop_ws
from .http_server import start_server as serve_http
from .http_server import stop as stop_http
COMMAND_GET_VAR = 'getvar'
COMMAND_GET_MPL = 'getmpl'

class Vis:

    def __init__(self, ws_port=8000, vis_port=80):
        self.ws_port = ws_port
        self.vis_port = vis_port
        self.pws = threaded(serve_ws, 'localhost', ws_port, self.handler)
        self.phttp = threaded(serve_http, vis_port)
        self.vars = {}
        self.cached_vars = {}

    def show(self):
        webbrowser.open(f"localhost:{self.vis_port}")

    def stop(self):
        print('Stopping websocket server')
        stop_ws()
        print('Stopping Http server')
        stop_http()

    def handler(self, message):
        try:
            command, args = message.split(':')
        except ValueError as e:
            try:
                return 'Wrong format'
            finally:
                e = None
                del e

        try:
            params = json.loads(args)
        except json.JSONDecodeError as e:
            try:
                params = {'varname': args}
            finally:
                e = None
                del e

        if command == 'get':
            var = params.get('varname')
            if var:
                val = self.vars.get(var)
                cache = self.cached_vars.get(var)
                if id(val) == cache:
                    return
                self.cached_vars[var] = id(val)
                try:
                    msg = ifc.get_var(val, params)
                    return msg
                except Exception as e:
                    try:
                        msg = ifc.get_var(str(e), params)
                        return msg
                    finally:
                        e = None
                        del e

        return 'Unknown command'