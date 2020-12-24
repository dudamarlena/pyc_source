# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/async/tests/test_async_tool.py
# Compiled at: 2020-01-16 15:18:07
# Size of source mod 2**32: 2825 bytes
import asyncio, sys
from unittest import TestCase

class TestAsyncTool(TestCase):

    @classmethod
    @asyncio.coroutine
    def countdown_coroutine(cls, number, n):
        while n > 0:
            print('T-minus', n, '({})'.format(number))
            yield from asyncio.sleep(1)
            n -= 1

        if False:
            yield None

    def test_01(self):
        cls = self.__class__

        def subtest(loop):
            self.assertFalse(loop.is_closed())
            tasks = [
             asyncio.ensure_future((cls.countdown_coroutine('A', 2)), loop=loop),
             asyncio.ensure_future((cls.countdown_coroutine('B', 3)), loop=loop)]
            loop.run_until_complete(asyncio.wait(tasks))
            print('hello world', file=(sys.stderr))

        loop_system = asyncio.get_event_loop()
        subtest(loop_system)
        loop_new = asyncio.new_event_loop()
        subtest(loop_new)
        loop_new.close()

    @classmethod
    async def countdown_async(cls, number, n):
        while n > 0:
            print('T-minus', n, '({})'.format(number))
            await asyncio.sleep(1)
            n -= 1

    def test_02(self):
        cls = self.__class__

        def subtest(loop):
            self.assertFalse(loop.is_closed())
            futures = [
             cls.countdown_async('A', 2),
             cls.countdown_async('B', 3)]
            loop.run_until_complete(asyncio.wait(futures))
            print('hello world', file=(sys.stderr))

        loop_system = asyncio.get_event_loop()
        subtest(loop_system)
        loop_new = asyncio.new_event_loop()
        subtest(loop_new)
        loop_new.close()

    def test_03(self):
        cls = self.__class__

        def subtest(loop):
            self.assertFalse(loop.is_closed())
            tasks = [
             asyncio.ensure_future((cls.countdown_async('A', 2)), loop=loop),
             asyncio.ensure_future((cls.countdown_async('B', 3)), loop=loop)]
            loop.run_until_complete((asyncio.gather)(*tasks))
            print('hello world', file=(sys.stderr))

        loop_system = asyncio.get_event_loop()
        subtest(loop_system)
        loop_new = asyncio.new_event_loop()
        subtest(loop_new)
        loop_new.close()