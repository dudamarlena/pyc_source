# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_unicode.py
# Compiled at: 2019-06-26 11:58:00
from unittest import TestCase
from pyutil import jsonutil as json
try:
    unichr = unichr
except NameError:
    unichr = chr

class TestUnicode(TestCase):

    def test_encoding1(self):
        encoder = json.JSONEncoder(encoding='utf-8')
        u = 'αΩ'
        s = u.encode('utf-8')
        ju = encoder.encode(u)
        js = encoder.encode(s)
        self.assertEqual(ju, js)

    def test_encoding2(self):
        u = 'αΩ'
        s = u.encode('utf-8')
        ju = json.dumps(u, encoding='utf-8')
        js = json.dumps(s, encoding='utf-8')
        self.assertEqual(ju, js)

    def test_encoding3(self):
        u = 'αΩ'
        j = json.dumps(u)
        self.assertEqual(j, '"\\u03b1\\u03a9"')

    def test_encoding4(self):
        u = 'αΩ'
        j = json.dumps([u])
        self.assertEqual(j, '["\\u03b1\\u03a9"]')

    def test_encoding5(self):
        u = 'αΩ'
        j = json.dumps(u, ensure_ascii=False)
        self.assertEqual(j, '"%s"' % (u,))

    def test_encoding6(self):
        u = 'αΩ'
        j = json.dumps([u], ensure_ascii=False)
        self.assertEqual(j, '["%s"]' % (u,))

    def test_big_unicode_encode(self):
        u = '𝄠'
        self.assertEqual(json.dumps(u), '"\\ud834\\udd20"')
        self.assertEqual(json.dumps(u, ensure_ascii=False), '"𝄠"')

    def test_big_unicode_decode(self):
        u = 'z𝄠x'
        self.assertEqual(json.loads('"' + u + '"'), u)
        self.assertEqual(json.loads('"z\\ud834\\udd20x"'), u)

    def test_unicode_decode(self):
        for i in range(0, 55295):
            u = unichr(i)
            js = '"\\u%04x"' % (i,)
            self.assertEqual(json.loads(js), u)