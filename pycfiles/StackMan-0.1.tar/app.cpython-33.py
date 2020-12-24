# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/app.py
# Compiled at: 2013-12-12 21:43:13
# Size of source mod 2**32: 1729 bytes
"""
StackMan
Application
Colton J. Provias - cj@coltonprovias.com
Created: December 8, 2013

The main application and web handler for StackMan.
"""
import logging, os, uuid, json
from tornado import options, web, ioloop
from .websocket import SocketHandler
options.define('port', default=6760, type=int, metavar='PORT', help='Port to bind to.')
options.define('file', default='stackman.stack', type=str, metavar='FILE', help='File to load and save stack to.')

class Application(web.Application):
    __doc__ = ' Create and initialize both the WebHandler and the SocketHandler. '

    def __init__(self):
        handlers = [('/', WebHandler),
         (
          '/socket', SocketHandler)]
        settings = {'cookie_secret': uuid.uuid4().hex,  'static_path': os.path.join(os.path.dirname(__file__), 'static')}
        SocketHandler.file = options.options.file
        SocketHandler.load_stacks()
        web.Application.__init__(self, handlers, **settings)


class WebHandler(web.RequestHandler):
    __doc__ = ' Display a simple page...with some messy JavaScript. '

    def get(self):
        self.render('templates/index.html')


def main():
    options.parse_command_line()
    if not os.path.exists(options.options.file):
        logging.warning('Configuration file not found.  Creating.')
        json.dump({'stacks': []}, open(options.options.file, 'w'))
    application = Application()
    application.listen(options.options.port)
    port = str(options.options.port)
    logging.warning('Now running at http://0.0.0.0:' + port)
    ioloop.IOLoop.instance().start()