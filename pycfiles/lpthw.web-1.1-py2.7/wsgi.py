# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/web/wsgi.py
# Compiled at: 2011-06-21 16:54:55
"""
WSGI Utilities
(from web.py)
"""
import os, sys, http, webapi as web
from utils import listget
from net import validaddr, validip
import httpserver

def runfcgi(func, addr=('localhost', 8000)):
    """Runs a WSGI function as a FastCGI server."""
    import flup.server.fcgi as flups
    return flups.WSGIServer(func, multiplexed=True, bindAddress=addr, debug=False).run()


def runscgi(func, addr=('localhost', 4000)):
    """Runs a WSGI function as an SCGI server."""
    import flup.server.scgi as flups
    return flups.WSGIServer(func, bindAddress=addr, debug=False).run()


def runwsgi(func):
    """
    Runs a WSGI-compatible `func` using FCGI, SCGI, or a simple web server,
    as appropriate based on context and `sys.argv`.
    """
    if os.environ.has_key('SERVER_SOFTWARE'):
        os.environ['FCGI_FORCE_CGI'] = 'Y'
    if os.environ.has_key('PHP_FCGI_CHILDREN') or os.environ.has_key('SERVER_SOFTWARE'):
        return runfcgi(func, None)
    else:
        if 'fcgi' in sys.argv or 'fastcgi' in sys.argv:
            args = sys.argv[1:]
            if 'fastcgi' in args:
                args.remove('fastcgi')
            else:
                if 'fcgi' in args:
                    args.remove('fcgi')
                if args:
                    return runfcgi(func, validaddr(args[0]))
            return runfcgi(func, None)
        if 'scgi' in sys.argv:
            args = sys.argv[1:]
            args.remove('scgi')
            if args:
                return runscgi(func, validaddr(args[0]))
            return runscgi(func)
        return httpserver.runsimple(func, validip(listget(sys.argv, 1, '')))


def _is_dev_mode():
    if os.environ.has_key('SERVER_SOFTWARE') or os.environ.has_key('PHP_FCGI_CHILDREN') or 'fcgi' in sys.argv or 'fastcgi' in sys.argv or 'mod_wsgi' in sys.argv:
        return False
    return True


web.config.setdefault('debug', _is_dev_mode())