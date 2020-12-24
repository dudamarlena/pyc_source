# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/msoucy/.virtualenv/restzzz/lib/python2.7/site-packages/restzzz/views.py
# Compiled at: 2014-09-25 17:09:31
""" Cornice services.
"""
import pyramid.exceptions as exc
from cornice import Service
import zmq
from pprint import pprint
from restzzz.zmqwrap import PubSocket, SubSocket
_SOCKETS_GET = {}
_SOCKETS_POST = {}
_CFG = {}
socklist = Service(name='socketlist', path='/', description='List sockets')
sockserv = Service(name='restzzz', path='/{queue}', description='RESTZZZ app')

@socklist.get()
def get_info(request):
    """ Returns the list of available endpoints. """
    return _CFG


@sockserv.get()
def get_sock(request):
    qname = request.matchdict['queue']
    if qname in _SOCKETS_GET:
        return _SOCKETS_GET[qname].recv()
    raise exc.NotFound


@sockserv.post()
def post_sock(request):
    qname = request.matchdict['queue']
    if qname in _SOCKETS_POST:
        return _SOCKETS_POST[qname].send(request.body)
    raise exc.NotFound


def load_sockets(cfg):
    _CFG.update(cfg)
    ctx = zmq.Context.instance()
    for name, settings in cfg.get('get', {}).items():
        _SOCKETS_GET[name] = SubSocket(settings['connect'], settings.get('subject', ''))

    for name, settings in cfg.get('post', {}).items():
        _SOCKETS_POST[name] = PubSocket(settings['connect'], settings.get('subject', None))

    return