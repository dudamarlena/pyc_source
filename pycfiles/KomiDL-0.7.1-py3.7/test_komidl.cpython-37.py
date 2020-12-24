# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_komidl.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 1234 bytes
"""Tests the Scraper class in KomiDL"""
import os, sys, argparse, unittest
from unittest import mock
sys.path.append(os.path.abspath('..'))
from komidl.komidl import KomiDL

class KomiDLTest(unittest.TestCase):
    __doc__ = 'Tests the KomiDL class in KomiDL'

    def setUp(self):
        """Create the KomiDL object for usage"""
        self.komidl = KomiDL(None)

    def test_get_extractor_valid(self):
        """Check if the appropriate extractors are returned for valid URLs

        This test re-uses URLs from the extractors to ensure that URLs are
        valid and the expected extractor is correct.
        """
        for extractor in self.komidl._extractors:
            with self.subTest(msg=f"For {extractor.name}EX URLS"):
                tests = extractor.get_tests()
                if not tests:
                    continue
                for test in tests:
                    actual_extr = self.komidl._get_extractor(test['url'])
                    expected_extr = extractor
                    with self.subTest(msg=f"URL={test['url']}"):
                        self.assertEqual(actual_extr.name, expected_extr.name)