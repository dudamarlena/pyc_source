# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/tests/test_json.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 802 bytes
import datetime
from aiohttp.test_utils import unittest_run_loop
from aiommy.json import dumps
from aiommy.unittest import AioTestCase

class JsonTestCase(AioTestCase):

    @unittest_run_loop
    async def test_datetime_json(self):
        data = {'date': datetime.datetime.now()}
        result = dumps(data)
        self.assertTrue(isinstance(result, str))

    @unittest_run_loop
    async def test_date_json(self):
        data = {'date': datetime.datetime.now()}
        result = dumps(data)
        self.assertTrue(isinstance(result, str))

    @unittest_run_loop
    async def test_bytes_json(self):
        data = {'bytes': bytes('bytesting'.encode('utf-8'))}
        result = dumps(data)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(not result.startswith("b'"))