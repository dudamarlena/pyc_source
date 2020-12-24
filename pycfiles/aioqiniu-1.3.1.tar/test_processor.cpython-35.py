# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jorgeramos/Projects/uphold/aiopype/tests/test_processor.py
# Compiled at: 2016-07-05 10:43:47
# Size of source mod 2**32: 1615 bytes
__doc__ = '\nTest processor.\n'
import asyncio
from unittest import TestCase
from aiopype import SyncProtocol
from aiopype.processor import Processor

class TestProcessor(TestCase):

    def test_emit_async(self):
        """
    Test processor's emit_async.
    """
        self.async_called = False
        self.sync_called = True

        async def async_handler():
            """
      Async handler.
      """
            await asyncio.sleep(1)
            self.async_called = True

        def sync_handler():
            """
      Sync handler.
      """
            self.sync_called = True

        async def run_emit():
            handled = await event_emitter.emit_async('test')
            self.assertTrue(handled)

        event_emitter = Processor('test', SyncProtocol())
        event_emitter.once('test', async_handler)
        event_emitter.once('test', sync_handler)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_emit())
        self.assertTrue(self.async_called)
        self.assertTrue(self.sync_called)

    def test_is_done(self):
        processor = Processor('test', SyncProtocol())
        self.assertFalse(processor.is_done())
        processor.done = True
        self.assertTrue(processor.is_done())

    def test_exception_without_handler(self):
        """
    Test exception without handler.
    """
        event_emitter = Processor('test', SyncProtocol())
        exception = None

        async def run_emit():
            await event_emitter.emit_async('error')

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run_emit())
        except Exception as err:
            exception = err

        self.assertEqual(str(exception), 'Uncaught error event.')