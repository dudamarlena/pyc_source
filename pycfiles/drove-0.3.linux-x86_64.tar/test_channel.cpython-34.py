# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/test_channel.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1643 bytes
import unittest
from drove.channel import Channel

class TestChannel(unittest.TestCase):

    def test_channel_subscription(self):
        """Testing Channel: subscription"""
        channel = Channel()
        channel.subscribe('test')
        assert 'test' in channel.queues

    def test_channel_broadcast(self):
        """Testing Channel: publish broadcast"""
        channel = Channel()
        channel.subscribe('test')
        channel.publish('hello')
        assert [x for x in channel.receive('test')][0] == 'hello'

    def test_channel_publish(self):
        """Testing Channel: publish topic"""
        channel = Channel()
        channel.subscribe('test')
        channel.subscribe('test2')
        channel.publish('hello', topic='test')
        assert [x for x in channel.receive('test')][0] == 'hello'
        assert channel.queues['test2'].qsize() == 0

    def test_channel_publish_none(self):
        """Testing Channel: publish non-existant"""
        channel = Channel()
        with self.assertRaises(KeyError):
            channel.publish('bye', topic='fail')

    def test_channel_receive_none(self):
        """Testing Channel: receive non-existant"""
        channel = Channel()
        channel.subscribe('test')
        channel.publish('bye')
        with self.assertRaises(KeyError):
            [x for x in channel.receive('bye')]

    def test_channel_receive_empty(self):
        """Testing Channel: receive in empty queue"""
        channel = Channel()
        channel.subscribe('test')
        assert [x for x in channel.receive('test')] == []