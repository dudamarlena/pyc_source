# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/Documents/workspace/Yeti/yeti/modules/triggers.py
# Compiled at: 2016-02-16 19:41:05
# Size of source mod 2**32: 2302 bytes
from yeti import Module
import asyncio

class Triggers(Module):

    def module_init(self):
        pass

    def on_rising_edge(self, value_poll, callback, poll_time=0.2, repeat=True):
        coro = self.wait_for_rising_edge(value_poll, callback, poll_time=poll_time, repeat=repeat)
        self.start_coroutine(coro)

    def on_value(self, value_poll, value_target, value_tolerance=None, callback=None, poll_time=0.2, repeat=True):
        coro = self.wait_for_value(value_poll, value_target, value_tolerance, callback, poll_time=poll_time)
        self.start_coroutine(coro)

    def compare_value(self, value, target, tolerance=None):
        if tolerance is None:
            return value == target
        return abs(value - target) <= tolerance

    async def wait_for_value(self, value_poll, value_target, value_tolerance=None, callback=None, poll_time=0.2, repeat=False):
        await self.wait_for_condition(lambda : self.compare_value(value_poll(), value_target, value_tolerance), callback=callback, poll_time=poll_time, repeat=False)

    async def wait_for_rising_edge(self, condition, callback=None, poll_time=0.2, repeat=False):
        while True:
            await self.wait_for_condition(lambda : not condition(), poll_time=poll_time)
            await self.wait_for_condition(condition, callback=callback, poll_time=poll_time)
            if not repeat:
                break
            await asyncio.sleep(0.2)

    async def wait_for_condition(self, condition, callback=None, poll_time=0.2, repeat=False):
        while True:
            while not condition():
                await asyncio.sleep(poll_time)

            if callback is None:
                break
            else:
                if asyncio.iscoroutine(callback):
                    await callback()
                else:
                    callback()
                if not repeat:
                    break
            await asyncio.sleep(0.2)