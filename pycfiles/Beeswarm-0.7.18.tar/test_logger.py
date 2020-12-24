# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/server/tests/test_logger.py
# Compiled at: 2016-11-12 07:38:04
import unittest, zmq.green, gevent, beeswarm
from beeswarm.server.reporting.base_logger import BaseLogger
from beeswarm.shared.message_enum import Messages
from beeswarm.shared.socket_enum import SocketNames

class LoggerTests(unittest.TestCase):

    def test_base_logger(self):
        beeswarm.shared.zmq_context = zmq.Context()
        context = beeswarm.shared.zmq_context
        processed_sessions_publisher = context.socket(zmq.PUB)
        processed_sessions_publisher.bind(SocketNames.PROCESSED_SESSIONS.value)
        test_list = []
        mock_logger = TestLogger({}, test_list)
        mock_logger.start()
        gevent.sleep()
        for _ in range(15):
            processed_sessions_publisher.send('TOPIC DATA')

        gevent.sleep(2)
        self.assertEqual(len(mock_logger.test_queue), 15)
        mock_logger.stop()
        mock_logger.get(block=True, timeout=2)
        processed_sessions_publisher.close()


class TestLogger(BaseLogger):

    def __init__(self, options, test_queue):
        super(TestLogger, self).__init__(options)
        self.test_queue = test_queue

    def handle_processed_session(self, topic, data):
        self.test_queue.append(data)