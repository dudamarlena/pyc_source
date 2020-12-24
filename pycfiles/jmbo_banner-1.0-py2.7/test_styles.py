# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/tests/test_styles.py
# Compiled at: 2018-01-09 13:54:21
from django.test import TestCase
from banner.styles import BANNER_STYLES_MAP, BANNER_STYLE_CLASSES, BaseStyle
from banner.tests.banner_config.styles import TestStyle

class BannerStyleTestCase(TestCase):
    """
    Verify that styles are discoverable and work as expected.
    A 'test style config' is configured to test this at
    banner.tests.banner_config
    """

    def test_custom_styles_can_be_discovered(self):
        self.assertTrue('TestStyle' in BANNER_STYLES_MAP)

    def test_no_duplicate_styles(self):
        self.assertEqual(len(BANNER_STYLE_CLASSES), 2)
        self.assertIn(TestStyle, BANNER_STYLE_CLASSES)
        self.assertIn(BaseStyle, BANNER_STYLE_CLASSES)