# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/consumers.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 4192 bytes
"""Deal with Xbus consumers.

In particular, save whether they provide data clearing and the database they
use.
"""
import aiozmq
from aiozmq import rpc
import asyncio
from copy import copy
import logging
from pyramid.httpexceptions import HTTPBadRequest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import uuid
from zope.sqlalchemy import ZopeTransactionExtension
from xbus.monitor.aiozmq_util import resolve_endpoint
log = logging.getLogger(__name__)

def _make_session(db_url):
    """Build an SQLAlchemy session object from a database URL."""
    return scoped_session(sessionmaker(bind=create_engine(db_url), extension=ZopeTransactionExtension()))


_consumers = []
_consumer_clearing_sessions = {}

def get_consumers():
    """Get the cached list of consumers. To retrieve an up-to-date list, call
    "refresh_consumers" first.

    :rtype: List of dicts.
    """
    global _consumers
    return copy(_consumers)


def get_consumer_clearing_session(consumer_id):
    """Get an SQLAlchemy session object bound to the data clearing database
    provided by the specified consumer.

    :param consumer_id: UID of the Xbus consumer.
    :type consumer_id: String.

    :raise HTTPBadRequest.

    :rtype: sqlalchemy.orm.scoped_session.
    """
    global _consumer_clearing_sessions
    if consumer_id:
        session = _consumer_clearing_sessions.get(consumer_id)
        if session:
            return session
    raise HTTPBadRequest(json_body={'error': 'Data clearing information missing.'})


@asyncio.coroutine
def _request_consumers(front_url, login, password, loop):
    """Ask Xbus for the list of consumers.

    :return: List of 2-element tuples (metadata dict, feature dict).
    """
    log.debug('Establishing RPC connection...')
    client = yield from rpc.connect_rpc(connect=front_url, loop=loop)
    log.debug('RPC connection OK')
    token = yield from client.call.login(login, password)
    log.debug('Got connection token: %s', token)
    consumers = yield from client.call.get_consumers(token)
    log.debug('Got the consumer list: %s', consumers)
    yield from client.call.logout(token)
    log.debug('Logged out; terminating')
    client.close()
    log.debug('Done.')
    return consumers


def refresh_consumers(request):
    """Ask Xbus for a fresh new list of Xbus consumers.
    """
    global _consumer_clearing_sessions
    global _consumers
    front_url = request.registry.settings['xbus.broker.front.url']
    login = request.registry.settings['xbus.broker.front.login']
    password = request.registry.settings['xbus.broker.front.password']
    front_url = resolve_endpoint(front_url)
    zmq_loop = aiozmq.ZmqEventLoopPolicy().new_event_loop()
    consumers_future = _request_consumers(front_url, login, password, zmq_loop)
    consumers_data = zmq_loop.run_until_complete(consumers_future)
    log.debug('Got consumers data: %s', consumers_data)
    _consumers = [{'clearing': bool(consumer_info[1]['clearing'][0]),  'id': uuid.uuid4().hex,  'name': consumer_info[0]['name']} for consumer_info in consumers_data if 'name' in consumer_info[0]]
    _consumer_clearing_sessions = {_consumers[consumer_index]['id']:_make_session(consumer_info[1]['clearing'][1]) for consumer_index, consumer_info in enumerate(consumers_data) if consumer_info[1]['clearing'][0] if consumer_info[1]['clearing'][0]}