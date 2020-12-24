# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/tests/dest_joke.py
# Compiled at: 2013-08-06 10:08:37
from unittest import TestCase
import dryxPython

class TestConvertFitsToDictionary(TestCase):

    def test_is_string(self):
        s = funniest.joke()
        self.assertTrue(isinstance(s, basestring))