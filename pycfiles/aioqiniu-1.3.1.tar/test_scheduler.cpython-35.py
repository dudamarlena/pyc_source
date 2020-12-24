# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jorgeramos/Projects/uphold/aiopype/tests/sources/test_scheduler.py
# Compiled at: 2016-07-05 10:43:47
# Size of source mod 2**32: 696 bytes
__doc__ = '\nTest scheduler sources.\n'
import asyncio
from unittest import TestCase
from aiopype.sources import CronJob
from aiopype import SyncProtocol

class TestScheduler(TestCase):

    def test_scheduler(self):
        mock_handler = SyncProtocol()
        scheduler = CronJob('cron', mock_handler, frequency=1, interval=1)
        timestamps = []

        def handler(timestamp):
            timestamps.append(timestamp)
            if len(timestamps) == 3:
                scheduler.done = True

        scheduler.on('cron', handler)
        asyncio.get_event_loop().run_until_complete(scheduler.start())
        self.assertEqual(timestamps[0], timestamps[1] - 1)
        self.assertEqual(timestamps[1], timestamps[2] - 1)