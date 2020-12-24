# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/extension/tests/test_extension.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase
from django.utils import six
from rbpowerpack.extension import PowerPackExtension

class PowerPackExtensionTests(LicensedExtensionTestCase):
    """Unit tests for rbpowerpack.extension.PowerPackExtension."""
    extension_class = PowerPackExtension

    def test_features_populate_attributes(self):
        """Testing PowerPackExtension attributes populated by features"""
        for feature_cls in self.extension.feature_classes:
            for css_bundle in six.iterkeys(feature_cls.css_bundles):
                self.assertIn(css_bundle, self.extension.css_bundles)

            for js_bundle in six.iterkeys(feature_cls.js_bundles):
                self.assertIn(js_bundle, self.extension.js_bundles)

            for key, value in six.iteritems(feature_cls.default_settings):
                self.assertIn(key, self.extension.default_settings)
                self.assertEqual(self.extension.default_settings[key], value)

            if feature_cls.enabled_settings_key:
                key = feature_cls.enabled_settings_key
                self.assertIn(key, self.extension.default_settings)
                self.assertEqual(self.extension.default_settings[key], feature_cls.enabled_by_default)