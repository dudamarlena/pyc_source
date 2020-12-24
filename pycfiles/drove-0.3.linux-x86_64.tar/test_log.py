# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/dev/me/drove/drove/plugins/droveio/log/test_log.py
# Compiled at: 2015-01-20 05:42:58
import unittest
from drove.config import Config
from drove.channel import Channel
from drove.data.value import Value
from . import log

class TestLogPlugin(unittest.TestCase):

    def test_log_plugin(self):
        config = Config()
        channel = Channel()
        channel.subscribe('droveio.log')
        channel.publish(Value('test', 0))
        kls = log.LogPlugin(config, channel)
        kls.plugin_name = 'droveio.log'
        kls.write(channel)