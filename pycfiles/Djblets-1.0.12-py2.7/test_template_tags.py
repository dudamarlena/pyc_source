# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/features/tests/test_template_tags.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.template import Context, Template, TemplateSyntaxError
from django.test import RequestFactory
from kgb import SpyAgency
from djblets.features import Feature, FeatureLevel, get_features_registry
from djblets.testing.testcases import TestCase

class IfFeatureTests(SpyAgency, TestCase):
    """Base class for ``{% if_feature_* %}`` template tag tests."""

    def setUp(self):
        super(IfFeatureTests, self).setUp()
        get_features_registry().reset()

    def tearDown(self):
        super(IfFeatureTests, self).tearDown()
        get_features_registry().reset()


class IfFeatureEnabledTagTests(IfFeatureTests):
    """Unit tests for the ``{% if_feature_enabled %}`` template tag."""

    def test_missing_arguments(self):
        """Testing if_feature_enabled template tag with missing arguments"""
        with self.assertRaises(TemplateSyntaxError):
            Template(b'{% load features %}{% if_feature_enabled %}enabled{% endif_feature_enabled %}')

    def test_extra_positional_arguments(self):
        """Testing if_feature_enabled template tag with extra positional
        arguments
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(b'{% load features %}{% if_feature_enabled "my-feature" bar %}enabled{% endif_feature_enabled %}')

    def test_keyword_arguments(self):
        """Testing if_feature_enabled template tag with keyword arguments"""

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.STABLE

        feature = DummyFeature()
        self.spy_on(feature.is_enabled)
        t = Template(b'{% load features %}{% if_feature_enabled "my-feature" i=42 s="abc" b=True %}enabled{% endif_feature_enabled %}')
        request = RequestFactory().get(b'/')
        self.assertEqual(t.render(Context({b'request': request})), b'enabled')
        self.assertTrue(feature.is_enabled.called_with(request=request, i=42, s=b'abc', b=True))

    def test_enabled(self):
        """Testing if_feature_enabled template tag with an enabled feature"""

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.STABLE

        DummyFeature()
        t = Template(b'{% load features %}{% if_feature_enabled "my-feature" %}enabled{% endif_feature_enabled %}')
        self.assertEqual(t.render(Context()), b'enabled')

    def test_disabled(self):
        """Testing if_feature_enabled template tag with a disabled feature"""

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.BETA

        DummyFeature()
        t = Template(b'{% load features %}{% if_feature_enabled "my-feature" %}enabled{% endif_feature_enabled %}')
        self.assertEqual(t.render(Context()), b'')

    def test_invalid_feature_id(self):
        """Testing if_feature_enabled template tag with an invalid feature ID
        """
        t = Template(b'{% load features %}{% if_feature_enabled "my-feature" %}enabled{% endif_feature_enabled %}')
        self.assertEqual(t.render(Context()), b'')

    def test_else_with_enabled(self):
        """Testing if_feature_enabled template tag with else block and an
        enabled feature
        """

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.STABLE

        DummyFeature()
        t = Template(b'{% load features %}{% if_feature_enabled "my-feature" %}enabled{% else %}disabled{% endif_feature_enabled %}')
        self.assertEqual(t.render(Context()), b'enabled')

    def test_else_with_disabled(self):
        """Testing if_feature_enabled template tag with else block and a
        disabled feature
        """

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.BETA

        DummyFeature()
        t = Template(b'{% load features %}{% if_feature_enabled "my-feature" %}enabled{% else %}disabled{% endif_feature_enabled %}')
        self.assertEqual(t.render(Context()), b'disabled')

    def test_else_with_invalid_feature_id(self):
        """Testing if_feature_enabled template tag with else block and an
        invalid feature ID
        """
        t = Template(b'{% load features %}{% if_feature_enabled "my-feature" %}enabled{% else %}disabled{% endif_feature_enabled %}')
        self.assertEqual(t.render(Context()), b'disabled')


class IfFeatureDisabledTagTests(IfFeatureTests):
    """Unit tests for the ``{% if_feature_disabled %}`` template tag."""

    def test_missing_arguments(self):
        """Testing if_feature_disabled template tag with missing arguments"""
        with self.assertRaises(TemplateSyntaxError):
            Template(b'{% load features %}{% if_feature_disabled %}enabled{% endif_feature_disabled %}')

    def test_extra_positional_arguments(self):
        """Testing if_feature_disabled template tag with extra positional
        arguments
        """
        with self.assertRaises(TemplateSyntaxError):
            Template(b'{% load features %}{% if_feature_disabled "my-feature" bar %}enabled{% endif_feature_disabled %}')

    def test_keyword_arguments(self):
        """Testing if_feature_disabled template tag with keyword arguments"""

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.BETA

        feature = DummyFeature()
        self.spy_on(feature.is_enabled)
        t = Template(b'{% load features %}{% if_feature_disabled "my-feature" i=42 s="abc" b=True %}disabled{% endif_feature_disabled %}')
        request = RequestFactory().get(b'/')
        self.assertEqual(t.render(Context({b'request': request})), b'disabled')
        self.assertTrue(feature.is_enabled.called_with(request=request, i=42, s=b'abc', b=True))

    def test_enabled(self):
        """Testing if_feature_disabled template tag with an enabled feature"""

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.STABLE

        DummyFeature()
        t = Template(b'{% load features %}{% if_feature_disabled "my-feature" %}disabled{% endif_feature_disabled %}')
        self.assertEqual(t.render(Context()), b'')

    def test_disabled(self):
        """Testing if_feature_disabled template tag with a disabled feature"""

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.BETA

        DummyFeature()
        t = Template(b'{% load features %}{% if_feature_disabled "my-feature" %}disabled{% endif_feature_disabled %}')
        self.assertEqual(t.render(Context()), b'disabled')

    def test_invalid_feature_id(self):
        """Testing if_feature_disabled template tag with an invalid feature ID
        """
        t = Template(b'{% load features %}{% if_feature_disabled "my-feature" %}disabled{% endif_feature_disabled %}')
        self.assertEqual(t.render(Context()), b'disabled')

    def test_else_with_enabled(self):
        """Testing if_feature_disabled template tag with else block and an
        enabled feature
        """

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.STABLE

        DummyFeature()
        t = Template(b'{% load features %}{% if_feature_disabled "my-feature" %}disabled{% else %}enabled{% endif_feature_disabled %}')
        self.assertEqual(t.render(Context()), b'enabled')

    def test_else_with_disabled(self):
        """Testing if_feature_disabled template tag with else block and a
        disabled feature
        """

        class DummyFeature(Feature):
            feature_id = b'my-feature'
            level = FeatureLevel.BETA

        DummyFeature()
        t = Template(b'{% load features %}{% if_feature_disabled "my-feature" %}disabled{% else %}enabled{% endif_feature_disabled %}')
        self.assertEqual(t.render(Context()), b'disabled')

    def test_else_with_invalid_feature_id(self):
        """Testing if_feature_disabled template tag with else block and an
        invalid feature ID
        """
        t = Template(b'{% load features %}{% if_feature_disabled "my-feature" %}disabled{% else %}enabled{% endif_feature_disabled %}')
        self.assertEqual(t.render(Context()), b'disabled')