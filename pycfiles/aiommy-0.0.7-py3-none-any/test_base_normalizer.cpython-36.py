# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/tests/test_base_normalizer.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 1162 bytes
from aiohttp.test_utils import unittest_run_loop
from aiommy.normalizers import BaseNormalizer
from aiommy.unittest import AioTestCase
from tests.fixtures import ExtendedTestModel

class BaseNormalizerTestCase(AioTestCase):

    def setUp(self):
        super().setUp()
        self.model = ExtendedTestModel
        self.normalizer = BaseNormalizer()
        self.instance = self.model(id=1, data1=1, data2='2')
        self.expected = {'id':1,  'data1':1,  'data2':'2'}

    @unittest_run_loop
    async def test_normalize_object(self):
        normalized = self.normalizer.normalize_object(self.instance)
        self.assertEqual(self.expected, normalized)

    @unittest_run_loop
    async def test_normalize(self):
        normalized = self.normalizer.normalize([self.instance, self.instance])
        self.assertEqual(normalized, [self.expected, self.expected])

    @unittest_run_loop
    async def test_fields_set(self):

        class FieldNormalizer(BaseNormalizer):
            fields = ('data1', )

        normalizer = FieldNormalizer()
        normalized = normalizer.normalize_object(self.instance)
        self.assertNotIn('data2', normalized)