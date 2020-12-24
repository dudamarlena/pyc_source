# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/ginsfsm/ginsfsm/examples/wsgi/simple_wsgi_server.py
# Compiled at: 2013-04-28 06:05:21
"""
Simple WSGI server
==================

It uses :class:`ginsfsm.protocols.wsgi.server.c_wsgi_server.GWsgiServer`.

You can run this file with ``gserve simple_wsgi_server.ini``

.. autofunction:: main

"""
import logging
logging.basicConfig(level=logging.DEBUG)
from ginsfsm.gaplic import GAplic
from ginsfsm.globals import set_global_app, set_global_main_gaplic
from ginsfsm.protocols.wsgi.server.c_wsgi_server import GWsgiServer

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    yield 'Hello World\n'


def paste_app_factory(global_config, **local_conf):
    return application


def main(global_config, **local_conf):
    """ Entry point to run with gserve (PasteDeploy)
    """
    if 'application' in local_conf:
        application = local_conf.pop('application')
    else:
        raise Exception('You must supply an wsgi application.')
    ga = GAplic(name='Wsgi-Example', roles='', **local_conf)
    set_global_main_gaplic(ga)
    ga.create_gobj('wsgi-server', GWsgiServer, ga, application=application)
    return ga


if __name__ == '__main__':
    local_conf = {'GObj.trace_mach': True, 'GObj.logger': logging, 
       'GSock.trace_dump': True, 
       'wsgi-server.host': '0.0.0.0', 
       'wsgi-server.port': 8002, 
       'application': 'wsgi-application'}
    set_global_app('wsgi-application', paste_app_factory({}, **local_conf))
    ga = main({}, **local_conf)
    try:
        ga.start()
    except (KeyboardInterrupt, SystemExit):
        print 'Program stopped'