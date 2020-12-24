# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/import_failure_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2193 bytes
import unittest
from unittest import mock
from .make import make
PROJECT_FAILURE1 = '\n{\n    "driver": {\n        "typename": "test.bibliopixel.failure.Failure",\n        "num": 12\n    },\n\n    "layout": {\n        "typename": "bibliopixel.layout.strip.Strip"\n    },\n\n    "animation": {\n        "typename": "bibliopixel.animation.tests.StripChannelTest"\n    }\n}\n'
PROJECT_FAILURE2 = '\n{\n    "driver": {\n        "typename": "test.bibliopixel.failure2.NON_EXISTENT",\n        "num": 12\n    },\n\n    "layout": {\n        "typename": "bibliopixel.layout.strip.Strip"\n    },\n\n    "animation": {\n        "typename": "bibliopixel.animation.tests.StripChannelTest"\n    }\n}\n'
PROJECT_FAILURE3 = '\n{\n    "driver": {\n        "typename": "test.NON_EXISTENT.Failure",\n        "num": 12\n    },\n\n    "layout": {\n        "typename": "bibliopixel.layout.strip.Strip"\n    },\n\n    "animation": {\n        "typename": "bibliopixel.animation.tests.StripChannelTest"\n    }\n}\n'
BAD_JSON_ERROR = '\nwhile parsing a flow node\nexpected the node content, but found \']\'\n  in "<unicode string>", line 1, column 2:\n    {]\n     ^\n'

class ImportFailureTest(unittest.TestCase):

    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', False)
    def test_bad_import_json(self):
        with self.assertRaises(Exception):
            make('{]')

    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', True)
    def test_bad_import_yaml(self):
        with self.assertRaises(Exception) as (e):
            make('{]')
        self.assertEqual(str(e.exception).strip(), BAD_JSON_ERROR.strip())

    def test_failure1(self):
        with self.assertRaises(ImportError) as (e):
            make(PROJECT_FAILURE1)
        self.assertEqual(e.exception.name, 'test.bibliopixel.failure.Failure')

    def test_failure2(self):
        with self.assertRaises(ImportError) as (e):
            make(PROJECT_FAILURE2)
        self.assertEqual(e.exception.name, 'test.bibliopixel.failure2.NON_EXISTENT')

    def test_failure3(self):
        with self.assertRaises(ImportError) as (e):
            make(PROJECT_FAILURE3)
        self.assertEqual(e.exception.name, 'test.NON_EXISTENT.Failure')