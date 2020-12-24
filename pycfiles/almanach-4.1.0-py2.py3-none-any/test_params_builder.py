# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/test/test_params_builder.py
# Compiled at: 2015-08-31 22:18:14
import alman, unittest

class TestParamsBuilder(unittest.TestCase):
    params = {'dog': 'dog-value', 
       'string': 'string-value'}

    def setUp(self):
        self.alt_params = {'cat': 'cat-value', 
           'string': 'alt-str-value'}
        self.merge_params = alman.apibits.ParamsBuilder.merge(self.params, self.alt_params)

    def test_merge_all_values(self):
        self.assertEqual(self.merge_params['dog'], self.params['dog'])
        self.assertEqual(self.merge_params['cat'], self.alt_params['cat'])
        self.assertIsNotNone(self.merge_params['string'])

    def test_merge_priority(self):
        self.assertEqual(self.merge_params['string'], self.alt_params['string'])