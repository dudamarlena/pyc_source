# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/tests/test_coding.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 430 bytes
from aiohttp.test_utils import unittest_run_loop
from aiommy.middlewares import decode, encode
from aiommy.unittest import AioTestCase

class CodingTestCase(AioTestCase):

    @unittest_run_loop
    async def coding_test(self):
        payload = {'id': 1}
        token = encode(payload)
        self.assertTrue(isinstance(token, str))
        decoded_payload = decode(token)
        self.assertTrue(payload == decoded_payload)