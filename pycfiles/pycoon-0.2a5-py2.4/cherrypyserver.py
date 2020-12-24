# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycoon\wsgi\frontend\cherrypyserver.py
# Compiled at: 2006-12-08 05:26:24
"""Usage: pycoon -s cherrypy <host> <port> [<pycoon.xconf absolute file URI>]"""
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