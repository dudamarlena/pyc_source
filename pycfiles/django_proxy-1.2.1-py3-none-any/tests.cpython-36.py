# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mjumbewu/Programming/projects/django-proxy/proxy/tests.py
# Compiled at: 2019-07-05 14:22:34
# Size of source mod 2**32: 1124 bytes
from django.test import TestCase
from proxy.views import make_absolute_location

class TestAbsoluteLocation(TestCase):

    def test_already_absolute(self):
        absurl = make_absolute_location('https://example.com/test/path', 'https://example2.com/next/test/path?with=qs')
        self.assertEquals(absurl, 'https://example2.com/next/test/path?with=qs')

    def test_scheme_relative(self):
        absurl = make_absolute_location('https://example.com/test/path', '//example2.com/next/test/path?with=qs')
        self.assertEquals(absurl, 'https://example2.com/next/test/path?with=qs')

    def test_host_relative(self):
        absurl = make_absolute_location('https://example.com/test/path', '/next/test/path?with=qs')
        self.assertEquals(absurl, 'https://example.com/next/test/path?with=qs')

    def test_path_relative(self):
        absurl = make_absolute_location('https://example.com/test/path', 'next/test/path?with=qs')
        self.assertEquals(absurl, 'https://example.com/test/next/test/path?with=qs')