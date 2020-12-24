# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/unit/queue/test_message.py
# Compiled at: 2011-03-19 21:05:04
import unittest
from chula import config
from chula.queue import mqueue
from chula.queue.messages import echo, mail, message
config = config.Config()

class Test_mqueue(unittest.TestCase):
    doctest = message

    def _add(self, module=echo):
        msg = module.Message()
        msg.message = 'payload'
        self.mqueue.add(msg)

    def setUp(self):
        self.mqueue = mqueue.MessageQueue(config)

    def tearDown(self):
        pass

    def test_add(self):
        self._add()