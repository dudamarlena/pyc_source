# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/test/checkerdemo.py
# Compiled at: 2018-07-11 18:15:31
"""Demonstration app for cherrypy.checker.

This application is intentionally broken and badly designed.
To demonstrate the output of the CherryPy Checker, simply execute
this module.
"""
import os, cherrypy
thisdir = os.path.dirname(os.path.abspath(__file__))

class Root:
    pass


if __name__ == '__main__':
    conf = {'/base': {'tools.staticdir.root': thisdir, 'throw_errors': True}, 
       '/base/static': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'static'}, 
       '/base/js': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'js'}, 
       '/base/static2': {'tools.staticdir.on': True, 'tools.staticdir.dir': '/static'}, 
       '/static3': {'tools.staticdir.on': True, 'tools.staticdir.dir': 'static'}, 
       '/unknown': {'toobles.gzip.on': True}, '/cpknown': {'cherrypy.tools.encode.on': True}, '/conftype': {'request.show_tracebacks': 14}, '/web': {'tools.unknown.on': True}, '/app1': {'server.socket_host': '0.0.0.0'}, 'global': {'server.socket_host': 'localhost'}, '[/extra_brackets]': {}}
    cherrypy.quickstart(Root(), config=conf)