# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/clue/bzrserver/main.py
# Compiled at: 2008-12-29 08:13:18
import logging, optparse, os, sys
from clue.bzrserver import server
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = '8080'
root = os.path.abspath(os.getcwd())
parts = [ x for x in os.path.split(root) if x ]
DEFAULT_CONFIGFILE = os.path.join(root, 'clue-bzrserver.ini')

def main(args=None, extraargs=None):
    logging.basicConfig()
    parser = optparse.OptionParser()
    parser.add_option('-p', '--port', dest='port', help='Port to listen on, defaults to %s' % DEFAULT_PORT, default=DEFAULT_PORT)
    parser.add_option('-i', '--interface', dest='host', help='Host to listen on, defaults to %s' % DEFAULT_HOST, default=DEFAULT_HOST)
    parser.add_option('-c', '--config', dest='configfile', help='Config file to use, defaults to %s' % DEFAULT_CONFIGFILE, default=DEFAULT_CONFIGFILE)
    parser.add_option('-a', '--authfile', dest='authfile', help='The passwd file to use for basic auth')
    if args is None:
        args = []
    if extraargs is None:
        extraargs = sys.argv[1:]
    (options, args) = parser.parse_args(args + extraargs)
    server.Server(configfile=options.configfile, host=options.host, port=options.port, passwdfile=options.authfile).run_server()
    return


if __name__ == '__main__':
    main()