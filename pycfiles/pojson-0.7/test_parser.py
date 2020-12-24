# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tests/test_parser.py
# Compiled at: 2016-08-25 17:03:17
from unittest import TestCase
from pojen import json_parser

class ParserTestCase(TestCase):

    def test_parses_json(self):
        json = '{"key":"val", "val": "key"}'
        data = json_parser.parse(json)
        self.assertEqual(type(data), dict)
        self.assertEqual(len(data), 2)
        self.assertEqual(data['key'], 'val')