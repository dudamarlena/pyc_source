# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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