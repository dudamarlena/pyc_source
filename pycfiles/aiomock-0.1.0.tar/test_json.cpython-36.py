# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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