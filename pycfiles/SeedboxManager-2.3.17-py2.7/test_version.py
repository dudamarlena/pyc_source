# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/test_version.py
# Compiled at: 2015-06-14 13:30:57
"""
Test case for version module
"""
from seedbox.tests import test
from seedbox import version

class VersionTest(test.BaseTestCase):

    def test_get_versioninfo(self):
        versioninfo = version.version_info
        self.assertIsNotNone(versioninfo)

    def test_version_str(self):
        self.assertIsNotNone(version.version_string())

    def test_release_str(self):
        self.assertIsNotNone(version.release_string())