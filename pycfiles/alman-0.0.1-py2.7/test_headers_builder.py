# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/test/test_headers_builder.py
# Compiled at: 2015-08-31 22:18:14
import alman, unittest

class TestHeadersBuilder(unittest.TestCase):
    headers = {'dog': 'dog-value'}

    def setUp(self):
        self.built_headers = alman.apibits.HeadersBuilder.build(self.headers)
        self.version = '0.0.2'

    def test_set_content_type(self):
        self.assertIn('Content-Type', self.built_headers)
        self.assertEqual('', self.built_headers['Content-Type'])

    def test_set_user_agent(self):
        self.assertIn('User-Agent', self.built_headers)
        self.assertIn('Alman', self.built_headers['User-Agent'])
        self.assertIn('0.0.1', self.built_headers['User-Agent'])