# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_encoders.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import json
from djblets.testing.testcases import TestCase
from djblets.webapi.encoders import JSONEncoderAdapter, WebAPIEncoder, XMLEncoderAdapter

class EncoderAdapterTests(TestCase):
    """Tests encoding correctness of WebAPIEncoder adapters"""
    data = {b'dict_val': {b'foo': b'bar'}, b'list_val': [
                   10, b'baz'], 
       b'string_val': b'foobar', 
       b'int_val': 42, 
       b'float_val': 3.14159, 
       b'scientific_val': 2.75e-15, 
       b'bool_val': True, 
       b'none_val': None}

    def test_json_encoder_adapter(self):
        """Testing JSONEncoderAdapter.encode"""
        encoder = WebAPIEncoder()
        adapter = JSONEncoderAdapter(encoder)
        content = adapter.encode(self.data)
        self.assertEqual(content, json.dumps(self.data))

    def test_xml_encoder_adapter(self):
        """Testing XMLEncoderAdapter.encode"""
        encoder = WebAPIEncoder()
        adapter = XMLEncoderAdapter(encoder)
        expected = b'<?xml version="1.0" encoding="utf-8"?>\n<rsp>\n <string_val>foobar</string_val>\n <none_val>\n </none_val>\n <dict_val>\n  <foo>bar</foo>\n </dict_val>\n <bool_val>1</bool_val>\n <scientific_val>2.75e-15</scientific_val>\n <int_val>42</int_val>\n <float_val>3.14159</float_val>\n <list_val>\n  <array>\n   <item>10</item>\n   <item>baz</item>\n  </array>\n </list_val>\n</rsp>'
        content = adapter.encode(self.data)
        self.assertEqual(content, expected)