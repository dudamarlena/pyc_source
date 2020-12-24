# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/tests/test_templatetags.py
# Compiled at: 2018-01-09 13:54:21
from django import template
from django.contrib.sites.models import Site
from django.http import Http404
from django.test import TestCase
from banner.models import Banner
from banner.styles import BANNER_STYLE_CLASSES

class TemplateTagTestCase(TestCase):
    fixtures = [
     'sites.json']

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagTestCase, cls).setUpTestData()
        cls.banner = Banner.objects.create(title='Test Banner', state='published', style=BANNER_STYLE_CLASSES[0].__name__)
        cls.banner.sites = list(Site.objects.all())
        cls.banner.publish()

    def test_renders_if_object_is_passed(self):
        context = template.Context({'banner': self.banner})
        t = template.Template('\n            {% load banner_tags %}\n            {% render_banner banner %}\n            ')
        result = t.render(context)
        self.failUnless('Test Banner' in result)

    def test_renders_if_slug_is_passed(self):
        context = template.Context({'banner': self.banner})
        t = template.Template('\n            {% load banner_tags %}\n            {% render_banner "test-banner" %}\n            ')
        result = t.render(context)
        self.failUnless('Test Banner' in result)

    def test_unknown_object_raises_404(self):
        with self.assertRaisesMessage(Http404, "No Banner with slug 'unknown-banner' was found"):
            t = template.Template('\n                {% load banner_tags %}\n                {% render_banner "unknown-banner" %}\n                ')
            t.render(template.Context({}))

    def test_raises_exception_if_banner_not_specified(self):
        with self.assertRaisesMessage(template.TemplateSyntaxError, "Tag usage: '{% render_banner <slug or object> %} '"):
            template.Template('\n                {% load banner_tags %}\n                {% render_banner %}\n                ')