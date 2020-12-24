# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/testing/testcases.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from beanbag_licensing.tests.testcases import LicensedExtensionTestCase
from django.utils.six.moves.urllib.parse import parse_qs, urlsplit
from rbpowerpack.extension import PowerPackExtension

class PowerPackExtensionTestCase(LicensedExtensionTestCase):
    """Base class for unit tests that test against an extension instance."""
    extension_class = PowerPackExtension

    def assertURLsEqual(self, url1, url2):
        """Assert whether two URLs are equal.

        This tests for strict equality in the base URL and path, and looser
        equality of the query string (same key/value pairs but independent
        of order.

        Args:
            url1 (unicode):
                The first URL to compare.

            url2 (unicode):
                The second URL to compare.
        """
        url_parts_1 = urlsplit(url1)
        url_parts_2 = urlsplit(url2)
        query_args_1 = parse_qs(url_parts_1.query)
        query_args_2 = parse_qs(url_parts_2.query)
        if url_parts_1.scheme != url_parts_2.scheme or url_parts_1.netloc != url_parts_2.netloc or url_parts_1.path != url_parts_2.path or url_parts_1.fragment != url_parts_2.fragment or query_args_1 != query_args_2:
            self.fail(b"'%s' != '%s'" % (url1, url2))


class FeaturelessPowerPackExtension(PowerPackExtension):
    """A Power Pack extension that doesn't load features by default.

    This is used for testing in :py:class:`FeatureTestCase`.
    """
    feature_classes = []


class FeatureTestCase(PowerPackExtensionTestCase):
    """Base class for unit tests for Feature classes."""
    extension_class = FeaturelessPowerPackExtension
    feature_class = None

    def setUp(self):
        super(FeatureTestCase, self).setUp()
        self.feature = self.feature_class(self.extension)

    def tearDown(self):
        super(FeatureTestCase, self).tearDown()
        if self.feature.enabled:
            self.feature.disable_feature()

    def check_enable(self, expected_hook_classes=[]):
        """Perform standard testing for the enable() method on a Feature."""
        self.assertFalse(self.feature.enabled)
        self.feature.enable_feature()
        self.assertTrue(self.feature.enabled)
        if expected_hook_classes:
            hook_classes = set([ hook.__class__ for hook in self.feature._hooks
                               ])
            self.assertEqual(hook_classes, set(expected_hook_classes))

    def check_disable(self):
        """Perform standard testing for the disable() method on a Feature."""
        self.feature.enable_feature()
        self.feature.disable_feature()
        self.assertFalse(self.feature.enabled)
        self.assertEqual(len(self.feature._hooks), 0)