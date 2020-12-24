# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/plonetheme/unam/tests/test_theme.py
# Compiled at: 2013-03-22 14:42:57
from plonetheme.unam.testing import THEMING_INTEGRATION_TESTING
import unittest2 as unittest

class TestIntegration(unittest.TestCase):
    layer = THEMING_INTEGRATION_TESTING

    def test_availableTheme(self):
        from plone.app.theming.utils import getTheme
        theme = getTheme('plonetheme.unam')
        self.assertTrue(theme is not None)
        self.assertEqual(theme.__name__, 'plonetheme.unam')
        self.assertEqual(theme.title, 'Theme UNAM')
        return