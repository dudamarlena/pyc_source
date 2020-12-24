# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pycoon\wsgi\frontend\cherrypyserver.py
# Compiled at: 2006-12-08 05:26:24
__doc__ = 'Usage: pycoon -s cherrypy <host> <port> [<pycoon.xconf absolute file URI>]'
__author__ = 'Andrey Nordin <http://claimid.com/anrienord>'
import sys, os
from pycoon.wsgi.servers.cherrypy.wsgiserver import CherryPyWSGIServer
from pycoon import wsgi

def main(*args):
    if len(args) == 2:
        from pkg_resources import resource_filename
        conf = resource_filename('pycoon', 'pycoon.xconf')
        if conf[0] != '/':
            conf = 'file:///%s' % conf.replace('\\', '/')
        else:
            conf = 'file://%s' % conf
    elif len(args) == 3:
        conf = args[2]
    else:
        print __doc__
        sys.exit(1)
    pycoon = wsgi.pycoonFactory({'server-xconf': conf})
    addr = (args[0], int(args[1]))
    server = CherryPyWSGIServer(addr, pycoon)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()