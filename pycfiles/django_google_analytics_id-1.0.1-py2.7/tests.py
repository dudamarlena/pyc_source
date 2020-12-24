# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\tests.py
# Compiled at: 2017-04-02 21:29:31
from django.conf import settings
from django.template import Template, Context
from django.test.testcases import TestCase
from django.test.utils import override_settings
from analytics.templatetags.analytics_tags import google_analytics

class GoogleAnalyticsTest(TestCase):

    @override_settings(GOOGLE_ANALYTICS_ID='UA-123-2')
    def test_default_id(self):
        self.assertFalse(hasattr(settings, 'DISABLE_GOOGLE_ANALYTICS'))
        code = google_analytics()
        self.assertIn('<script>', code)
        self.assertIn('UA-123-2', code)

    def test_no_default_id(self):
        self.assertFalse(hasattr(settings, 'DISABLE_GOOGLE_ANALYTICS'))
        self.assertRaises(AttributeError, google_analytics)

    def test_google_analytics_id(self):
        self.assertFalse(hasattr(settings, 'DISABLE_GOOGLE_ANALYTICS'))
        code = google_analytics('UA-123-1')
        self.assertIn('<script>', code)
        self.assertIn('UA-123-1', code)

    @override_settings(CODE='UA-123-2')
    def test_settings(self):
        self.assertFalse(hasattr(settings, 'DISABLE_GOOGLE_ANALYTICS'))
        code = google_analytics('CODE')
        self.assertIn('<script>', code)
        self.assertIn('UA-123-2', code)

    @override_settings(DISABLE_GOOGLE_ANALYTICS=False)
    def test_enabled_1(self):
        code = google_analytics('UA-123-1')
        self.assertIn('<script>', code)
        self.assertIn('UA-123-1', code)

    @override_settings(DISABLE_GOOGLE_ANALYTICS=False, CODE='UA-123-2')
    def test_enabled_2(self):
        code = google_analytics('CODE')
        self.assertIn('<script>', code)
        self.assertNotIn('CODE', code)
        self.assertNotIn('code', code)
        self.assertIn('UA-123-2', code)

    @override_settings(DISABLE_GOOGLE_ANALYTICS=True)
    def test_disabled_1(self):
        code = google_analytics('UA-123-1')
        self.assertEqual(code, '')

    @override_settings(DISABLE_GOOGLE_ANALYTICS=True, CODE='UA-123-2')
    def test_disabled_2(self):
        code = google_analytics('CODE')
        self.assertEqual(code, '')

    def test_render_template_1(self):
        t = Template('{% load analytics_tags %}\n            {% google_analytics %}"\n            ')
        self.assertRaises(AttributeError, t.render, Context())

    @override_settings(GOOGLE_ANALYTICS_ID='UA-123-2')
    def test_render_template_2(self):
        t = Template('{% load analytics_tags %}\n            {% google_analytics %}"\n            ')
        code = t.render(Context())
        self.assertIn('<script>', code)
        self.assertIn('UA-123-2', code)

    @override_settings(CODE='UA-123-1', GOOGLE_ANALYTICS_ID='UA-123-2')
    def test_render_template_3(self):
        t = Template('{% load analytics_tags %}\n            {% google_analytics "CODE" %}"\n            ')
        code = t.render(Context())
        self.assertIn('<script>', code)
        self.assertIn('UA-123-1', code)

    def test_render_template_4(self):
        t = Template('{% load analytics_tags %}\n            {% google_analytics "UA-123-3" %}"\n            ')
        code = t.render(Context())
        self.assertIn('<script>', code)
        self.assertIn('UA-123-3', code)

    @override_settings(DISABLE_GOOGLE_ANALYTICS=True)
    def test_render_template_5(self):
        t = Template('{% load analytics_tags %}{% google_analytics "CODE" %}')
        code = t.render(Context())
        self.assertEqual(code, '')