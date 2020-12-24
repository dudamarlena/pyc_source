# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/runserver.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
import sys, logging
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server
from ...command import SubCommand
from ...wsgi import WSGIApplication
from ...compat import socketserver
from ...compat import PY2
if PY2:
    from thread import interrupt_main
else:
    from _thread import interrupt_main
log = logging.getLogger(b'moya.runtime')

class RequestHandler(WSGIRequestHandler):

    def log_message(self, format, *args):
        pass


class ThreadedWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    daemon_threads = True


class ForkingWSGIServer(socketserver.ForkingMixIn, WSGIServer):
    pass


class Runserver(SubCommand):
    """Run a local Moya development server"""
    help = b'run a development server'

    def add_arguments(self, parser):
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to project settings file')
        parser.add_argument(b'-s', b'--server', dest=b'server', default=b'main', metavar=b'SERVERREF', help=b'server element to use')
        parser.add_argument(b'-H', b'--host', dest=b'host', default=b'127.0.0.1', help=b'IP address to bind to')
        parser.add_argument(b'-p', b'--port', dest=b'port', default=b'8000', help=b'port to listen on')
        parser.add_argument(b'-b', b'--breakpoint', dest=b'breakpoint', action=b'store_true', default=False, help=b'enter debug mode on every view')
        parser.add_argument(b'--no-validate', dest=b'novalidate', action=b'store_true', default=False, help=b"don't validate database models before running server")
        parser.add_argument(b'--breakpoint-startup', dest=b'breakpoint_startup', action=b'store_true', default=False, help=b'debug startup process')
        parser.add_argument(b'--no-reload', dest=b'noreload', action=b'store_true', default=False, help=b'disable auto-reload')
        parser.add_argument(b'--slow', dest=b'slow', action=b'store_true', default=False, help=b'simulate network latency by inserting delays')
        parser.add_argument(b'--debug-memory', dest=b'debug_memory', action=b'store_true', default=False, help=b'write log information to help identify memory leaks')
        parser.add_argument(b'--strict', dest=b'strict', action=b'store_true', default=False, help=b"enable 'strict' checking of tag attributes")
        parser.add_argument(b'-t', b'--use-threads', dest=b'usethreads', action=b'store_true', default=False, help=b'enable multi-threaded server')
        parser.add_argument(b'-d', b'--develop', dest=b'develop', action=b'store_true', default=False, help=b'enable develop mode for debugging Moya server')
        return parser

    def run(self):
        super(Runserver, self).run()
        args = self.args
        application = WSGIApplication(self.location, self.get_settings(), args.server, breakpoint=args.breakpoint, breakpoint_startup=args.breakpoint_startup, validate_db=not args.novalidate, disable_autoreload=self.args.noreload, simulate_slow_network=self.args.slow, debug_memory=self.args.debug_memory, strict=self.args.strict, develop=self.args.develop)
        application.preflight()
        try:
            server_class = WSGIServer
            if args.usethreads:
                server_class = ThreadedWSGIServer
                log.info(b'using multi threaded server')
            server = make_server(args.host, int(args.port), application, server_class=server_class, handler_class=RequestHandler)
        except IOError as e:
            if e.errno in (48, 98):
                log.critical(b"couldn't run moya server, another process may be running on port %s", args.port)
            raise

        if self.args.slow:
            log.info(b'network latency simulation is enabled')
        log.info((b'development server started on http://{}:{}').format(args.host, args.port))

        def handle_error(request, client_address):
            _type, value, tb = sys.exc_info()
            if isinstance(value, KeyboardInterrupt):
                interrupt_main()

        server.handle_error = handle_error
        try:
            server.serve_forever()
        finally:
            log.debug(b'user exit')
            application.close()