# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/features/tests/test_feature.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from kgb import SpyAgency
from django.conf import settings
from djblets.features import Feature, FeatureLevel, get_features_registry
from djblets.features.checkers import BaseFeatureChecker, get_feature_checker, set_feature_checker
from djblets.testing.testcases import TestCase

class DummyFeature(Feature):
    feature_id = b'djblets.tests.dummy-feature'
    name = b'Dummy Feature'
    summary = b'This is a dummy feature.'
    level = FeatureLevel.BETA

    def initialize(self):
        self._feature_inited = True

    def shutdown(self):
        self._feature_inited = False


class FeatureTests(SpyAgency, TestCase):
    """Unit tests for djblets.features.feature.Feature."""

    def setUp(self):
        super(FeatureTests, self).setUp()
        self._old_debug = settings.DEBUG

    def tearDown(self):
        super(FeatureTests, self).tearDown()
        settings.DEBUG = self._old_debug
        get_features_registry().reset()
        set_feature_checker(None)
        return

    def test_init_registers(self):
        """Testing Feature.__init__ registers the feature"""
        features = get_features_registry()
        self.assertEqual(len(features), 0)
        feature = DummyFeature()
        self.assertEqual(len(features), 1)
        self.assertIn(feature, features)

    def test_init_calls_initialize(self):
        """Testing Feature.__init__ calls initialize"""
        feature = DummyFeature()
        self.assertTrue(getattr(feature, b'_feature_inited', False))

    def test_is_enabled_with_stable(self):
        """Testing Feature.is_enabled with level=STABLE"""

        class StableFeature(DummyFeature):
            level = FeatureLevel.STABLE

        checker = get_feature_checker()
        feature = StableFeature()
        self.spy_on(checker.is_feature_enabled)
        self.assertTrue(feature.is_enabled())
        self.assertFalse(checker.is_feature_enabled.spy.called)

    def test_is_enabled_with_beta_debug_true(self):
        """Testing Feature.is_enabled with level=BETA and DEBUG=True"""

        class BetaFeature(DummyFeature):
            level = FeatureLevel.BETA

        feature = BetaFeature()
        settings.DEBUG = True
        self.assertTrue(feature.is_enabled())

    def test_is_enabled_with_beta_debug_false(self):
        """Testing Feature.is_enabled with level=BETA and DEBUG=False"""

        class BetaFeature(DummyFeature):
            level = FeatureLevel.BETA

        feature = BetaFeature()
        settings.DEBUG = False
        self.assertFalse(feature.is_enabled())

    def test_is_enabled_with_unavailable(self):
        """Testing Feature.is_enabled with level=UNAVAILABLE"""

        class UnavailableFeature(DummyFeature):
            level = FeatureLevel.UNAVAILABLE

        feature = UnavailableFeature()
        self.spy_on(get_feature_checker, call_original=False)
        self.assertFalse(feature.is_enabled())
        self.assertFalse(get_feature_checker.spy.called)

    def test_is_enabled_with_checker_true(self):
        """Testing Feature.is_enabled with feature checker returning True"""

        class DummyFeatureChecker(BaseFeatureChecker):

            def is_feature_enabled(self, feature_id, **kwargs):
                return True

        set_feature_checker(DummyFeatureChecker())
        feature = DummyFeature()
        self.assertTrue(feature.is_enabled())

    def test_is_enabled_with_checker_false(self):
        """Testing Feature.is_enabled with feature checker returning False"""

        class DummyFeatureChecker(BaseFeatureChecker):

            def is_feature_enabled(self, feature_id, **kwargs):
                return False

        set_feature_checker(DummyFeatureChecker())
        feature = DummyFeature()
        self.assertFalse(feature.is_enabled())