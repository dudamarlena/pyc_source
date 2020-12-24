# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robin/git/runwsgi/runwsgi/runwsgi.py
# Compiled at: 2016-05-02 11:21:40
"""
@author: sintrb
"""
__version__ = '0.0.2'
import sys, os
from wsgiref.simple_server import make_server

def print_help():
    print 'Usage: python -m runwsgi [-d workdir] [-b host:port] [-p "params"] model:applicaon'
    print 'Report bugs to <sintrb@gmail.com>'


def main():
    import getopt
    opts, args = getopt.getopt(sys.argv[1:], 'hb:p:d:')
    host = '0.0.0.0'
    port = 8000
    workdir = os.getcwd()
    for opt, arg in opts:
        if opt == '-b':
            if ':' in arg:
                host, port = arg.split(':')
                port = int(port)
            else:
                port = int(arg)
        elif opt == '-p':
            os.environ.setdefault('WSGI_PARAMS', arg)
        elif opt == '-d':
            workdir = arg
        elif opt == '-h':
            print_help()
            exit()

    if len(args) == 0:
        print_help()
        exit(-1)
    app_path = args[0]
    modules, application = app_path.split(':')
    sys.path.insert(0, workdir)
    module = __import__(modules)
    for m in modules.split('.')[1:]:
        module = getattr(module, m)

    application = getattr(module, application)
    httpd = make_server(host, port, application)
    print ('Serving HTTP on {host}:{port}...').format(host=host, port=port)
    httpd.serve_forever()


if __name__ == '__main__':
    main()