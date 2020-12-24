# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/pagepress/command.py
# Compiled at: 2012-03-23 03:34:40
import sys, os, logging, posixpath, urllib
from logging.config import fileConfig
from ConfigParser import SafeConfigParser
from pagepress.generator import Generator
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
usage = '\nUsage:\n    pagepress generate INI_FILE\n    pagepress serve INI_FILE\n    '
log = logging.getLogger(__name__)

def generate(config, base):
    g = Generator(base)
    g.update()


class PagepressHTTPHandler(SimpleHTTPRequestHandler):

    def do_GET(self, *args, **kwargs):
        generate(self.pagepress_config, self.pagepress_base)
        return SimpleHTTPRequestHandler.do_GET(self, *args, **kwargs)

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Ripped off from SimpleHTTPRequestHandler

        """
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.path.join(self.pagepress_base, 'static')
        for word in words:
            (drive, word) = os.path.splitdrive(word)
            (head, word) = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)

        return path


def serve(config, base):
    server_address = ('', 6554)
    PagepressHTTPHandler.pagepress_base = base
    PagepressHTTPHandler.pagepress_config = config
    httpd = HTTPServer(server_address, PagepressHTTPHandler)
    sa = httpd.socket.getsockname()
    log.info('Serving HTTP on %s:%s' % (sa[0], sa[1]))
    httpd.serve_forever()


def command():
    if len(sys.argv) != 3:
        print 'Invalid arguments'
        print usage
        sys.exit(1)
    command = sys.argv[1]
    config_file = sys.argv[2]
    if not os.path.isfile(config_file):
        print 'Invalid Config File'
        print usage
        sys.exit(1)
    config_file = os.path.abspath(config_file)
    parser = SafeConfigParser()
    parser.read([config_file])
    fileConfig([config_file])
    if parser.has_option('generate:main', 'base'):
        base = parser.get_option('generate:main', 'base')
    else:
        base = os.path.dirname(config_file)
    if command == 'generate':
        generate(parser, base)
    elif command == 'serve':
        serve(parser, base)
    else:
        print 'Invalid Command'
        print usage
        sys.exit(1)