# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/server/reporting/base_logger.py
# Compiled at: 2016-11-12 07:38:04
import logging
from gevent import Greenlet
from beeswarm.shared.socket_enum import SocketNames
import zmq.green, beeswarm
logger = logging.getLogger(__name__)

class BaseLogger(Greenlet):

    def __init__(self, options):
        Greenlet.__init__(self)
        self.enabled = True
        self.options = options

    def _run(self):
        context = beeswarm.shared.zmq_context
        processed_sessions_socket = context.socket(zmq.SUB)
        processed_sessions_socket.connect(SocketNames.PROCESSED_SESSIONS.value)
        processed_sessions_socket.setsockopt(zmq.SUBSCRIBE, '')
        live_sessions_socket = context.socket(zmq.SUB)
        live_sessions_socket.connect(SocketNames.DRONE_DATA.value)
        live_sessions_socket.setsockopt(zmq.SUBSCRIBE, 'SESSION_PART')
        poller = zmq.Poller()
        poller.register(processed_sessions_socket, zmq.POLLIN)
        poller.register(live_sessions_socket, zmq.POLLIN)
        while self.enabled:
            socks = dict(poller.poll(1000))
            if processed_sessions_socket in socks and socks[processed_sessions_socket] == zmq.POLLIN:
                topic, data = processed_sessions_socket.recv().split(' ', 1)
                self.handle_processed_session(topic, data)
            elif live_sessions_socket in socks and socks[live_sessions_socket] == zmq.POLLIN:
                topic, data = live_sessions_socket.recv().split(' ', 1)
                self.handle_live_session_part(topic, data)

        live_sessions_socket.close()
        processed_sessions_socket.close()

    def stop(self):
        self.enabled = False

    def handle_processed_session(self, topic, data):
        raise NotImplementedError('Please implement this method')

    def handle_live_session_part(self, topic, data):
        raise NotImplementedError('Please implement this method')