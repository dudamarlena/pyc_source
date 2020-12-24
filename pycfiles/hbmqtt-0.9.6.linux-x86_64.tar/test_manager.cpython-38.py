# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/tests/plugins/test_manager.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 3299 bytes
import unittest, logging, asyncio
from hbmqtt.plugins.manager import PluginManager
formatter = '[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(level=(logging.INFO), format=formatter)

class TestPlugin:

    def __init__(self, context):
        self.context = context


class EventTestPlugin:

    def __init__(self, context):
        self.context = context
        self.test_flag = False
        self.coro_flag = False

    @asyncio.coroutine
    def on_test(self, *args, **kwargs):
        self.test_flag = True
        self.context.logger.info('on_test')

    @asyncio.coroutine
    def test_coro(self, *args, **kwargs):
        self.coro_flag = True

    @asyncio.coroutine
    def ret_coro(self, *args, **kwargs):
        return 'TEST'


class TestPluginManager(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def test_load_plugin(self):
        manager = PluginManager('hbmqtt.test.plugins', context=None)
        self.assertTrue(len(manager._plugins) > 0)

    def test_fire_event(self):

        @asyncio.coroutine
        def fire_event():
            (yield from manager.fire_event('test'))
            (yield from asyncio.sleep(1, loop=(self.loop)))
            (yield from manager.close())
            if False:
                yield None

        manager = PluginManager('hbmqtt.test.plugins', context=None, loop=(self.loop))
        self.loop.run_until_complete(fire_event())
        plugin = manager.get_plugin('event_plugin')
        self.assertTrue(plugin.object.test_flag)

    def test_fire_event_wait(self):

        @asyncio.coroutine
        def fire_event():
            (yield from manager.fire_event('test', wait=True))
            (yield from manager.close())
            if False:
                yield None

        manager = PluginManager('hbmqtt.test.plugins', context=None, loop=(self.loop))
        self.loop.run_until_complete(fire_event())
        plugin = manager.get_plugin('event_plugin')
        self.assertTrue(plugin.object.test_flag)

    def test_map_coro(self):

        @asyncio.coroutine
        def call_coro():
            (yield from manager.map_plugin_coro('test_coro'))
            if False:
                yield None

        manager = PluginManager('hbmqtt.test.plugins', context=None, loop=(self.loop))
        self.loop.run_until_complete(call_coro())
        plugin = manager.get_plugin('event_plugin')
        self.assertTrue(plugin.object.test_coro)

    def test_map_coro_return(self):

        @asyncio.coroutine
        def call_coro():
            return (yield from manager.map_plugin_coro('ret_coro'))
            if False:
                yield None

        manager = PluginManager('hbmqtt.test.plugins', context=None, loop=(self.loop))
        ret = self.loop.run_until_complete(call_coro())
        plugin = manager.get_plugin('event_plugin')
        self.assertEqual(ret[plugin], 'TEST')

    def test_map_coro_filter(self):
        """
        Run plugin coro but expect no return as an empty filter is given
        :return:
        """

        @asyncio.coroutine
        def call_coro():
            return (yield from manager.map_plugin_coro('ret_coro', filter_plugins=[]))
            if False:
                yield None

        manager = PluginManager('hbmqtt.test.plugins', context=None, loop=(self.loop))
        ret = self.loop.run_until_complete(call_coro())
        self.assertTrue(len(ret) == 0)