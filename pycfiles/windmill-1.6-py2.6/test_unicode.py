# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_simplejson/tests/test_unicode.py
# Compiled at: 2011-01-13 01:48:00
from unittest import TestCase
import simplejson as json

class TestUnicode(TestCase):

    def test_encoding1(self):
        encoder = json.JSONEncoder(encoding='utf-8')
        u = 'αΩ'
        s = u.encode('utf-8')
        ju = encoder.encode(u)
        js = encoder.encode(s)
        self.assertEquals(ju, js)

    def test_encoding2(self):
        u = 'αΩ'
        s = u.encode('utf-8')
        ju = json.dumps(u, encoding='utf-8')
        js = json.dumps(s, encoding='utf-8')
        self.assertEquals(ju, js)

    def test_encoding3(self):
        u = 'αΩ'
        j = json.dumps(u)
        self.assertEquals(j, '"\\u03b1\\u03a9"')

    def test_encoding4(self):
        u = 'αΩ'
        j = json.dumps([u])
        self.assertEquals(j, '["\\u03b1\\u03a9"]')

    def test_encoding5(self):
        u = 'αΩ'
        j = json.dumps(u, ensure_ascii=False)
        self.assertEquals(j, '"%s"' % (u,))

    def test_encoding6(self):
        u = 'αΩ'
        j = json.dumps([u], ensure_ascii=False)
        self.assertEquals(j, '["%s"]' % (u,))

    def test_big_unicode_encode(self):
        u = '𝄠'
        self.assertEquals(json.dumps(u), '"\\ud834\\udd20"')
        self.assertEquals(json.dumps(u, ensure_ascii=False), '"𝄠"')

    def test_big_unicode_decode(self):
        u = 'z𝄠x'
        self.assertEquals(json.loads('"' + u + '"'), u)
        self.assertEquals(json.loads('"z\\ud834\\udd20x"'), u)

    def test_unicode_decode(self):
        for i in range(0, 55295):
            u = unichr(i)
            s = '"\\u%04x"' % (i,)
            self.assertEquals(json.loads(s), u)

    def test_default_encoding(self):
        self.assertEquals(json.loads(('{"a": "é"}').encode('utf-8')), {'a': 'é'})

    def test_unicode_preservation(self):
        self.assertEquals(type(json.loads('""')), unicode)
        self.assertEquals(type(json.loads('"a"')), unicode)
        self.assertEquals(type(json.loads('["a"]')[0]), unicode)