# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/showform.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import print_function
from __future__ import unicode_literals
import logging, sys
from os.path import abspath, dirname
from urllib import urlencode, quote
import webbrowser
from fs.opener import open_fs
from ...context import Context
from ...command import SubCommand
from ...wsgi import WSGIApplication
from ...compat import socketserver
from ...compat import PY2
if PY2:
    from thread import interrupt_main
else:
    from _thread import interrupt_main
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server
log = logging.getLogger(b'moya.runtime')

class RequestHandler(WSGIRequestHandler):

    def log_message(self, format, *args):
        pass


class ThreadedWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    daemon_threads = True


class Showform(SubCommand):
    """Show a form from the project"""
    help = b'show a form from the project'

    def add_arguments(self, parser):
        parser.add_argument(dest=b'formelement', metavar=b'ELEMENTREF', help=b'form element reference')
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to project settings file')
        parser.add_argument(b'-s', b'--server', dest=b'server', default=b'main', metavar=b'SERVERREF', help=b'server element to use')
        parser.add_argument(b'-H', b'--host', dest=b'host', default=b'127.0.0.1', help=b'IP address to bind to')
        parser.add_argument(b'-p', b'--port', dest=b'port', default=b'8001', help=b'port to listen on')
        parser.add_argument(b'-d', b'--develop', dest=b'develop', action=b'store_true', default=False, help=b'enable develop mode for debugging Moya server')
        return parser

    @classmethod
    def _post_build(cls, application):
        lib = application.archive.load_library_from_module(b'moya.libs.showform', priority=100, template_priority=100)
        application.archive.build_libs()
        context = Context()
        application.archive.call(b'moya.showform#install', context, b'__showform__', server=application.server)

    def run(self):
        super(Showform, self).run()
        args = self.args
        application = WSGIApplication(self.location, self.get_settings(), args.server, validate_db=False, develop=self.args.develop, post_build_hook=self._post_build)
        form_app, form = application.archive.get_element(args.formelement)
        log.info((b'testing {form} in {form_app}').format(form=form, form_app=form_app))
        server = make_server(args.host, int(args.port), application, server_class=ThreadedWSGIServer, handler_class=RequestHandler)

        def handle_error(request, client_address):
            _type, value, tb = sys.exc_info()
            if isinstance(value, KeyboardInterrupt):
                interrupt_main()

        server.handle_error = handle_error
        formelement_quoted = quote(args.formelement)
        url = (b'http://{}:{}/moya-show-form/form/{}/').format(args.host, args.port, formelement_quoted)
        log.info(b'opening %s', url)
        webbrowser.open(url)
        try:
            server.serve_forever()
        finally:
            log.debug(b'user exit')
            application.close()