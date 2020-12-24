# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\rodrigo\github\libextract\libextract\tests\test_libextract.py
# Compiled at: 2015-04-09 13:21:49
import os
from unittest import TestCase
from tests import asset_path
from libextract import extract
FOOS_FILENAME = asset_path('full_of_foos.html')

class TestLibExtract(TestCase):

    def setUp(self):
        with open(FOOS_FILENAME, 'rb') as (fp):
            self.content = extract(fp.read())

    def test_is_str(self):
        assert isinstance(self.content, str)

    def test_str_is_foos(self):
        foos = 'foo. foo. foo. foo. foo. foo. foo. foo. foo.'
        assert self.content == foos