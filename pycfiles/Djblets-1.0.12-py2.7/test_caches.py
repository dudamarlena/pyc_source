# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/template/tests/test_caches.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.conf import settings
from django.template import Context, Template, TemplateSyntaxError
from django.template.loader import get_template
from django.template.loaders.cached import Loader as CachedLoader
try:
    from django.apps.registry import apps
except ImportError:
    apps = None

try:
    from django.template.base import get_templatetags_modules
except ImportError:
    get_templatetags_modules = None

try:
    from django.template import engines
except ImportError:
    engines = None

from djblets.template.caches import clear_template_caches, clear_template_tag_caches
from djblets.testing.testcases import TestCase

class CachesTests(TestCase):
    """Unit tests for djblets.template.caches."""

    def test_clear_template_tag_caches(self):
        """Testing clear_template_tag_caches"""

        def _check_state(enabled):
            if enabled:
                if get_templatetags_modules is not None:
                    self.assertIn(templatetags_module_name, get_templatetags_modules())
                self.assertEqual(Template(template_str).render(Context({})), b'Hello, world!')
            else:
                if get_templatetags_modules is not None:
                    self.assertNotIn(templatetags_module_name, get_templatetags_modules())
                with self.assertRaisesRegexp(TemplateSyntaxError, b'is not a (valid|registered) tag library'):
                    Template(template_str).render(Context({}))
            return

        templatetags_module_name = b'djblets.template.tests.templatetags'
        template_str = b'{% load template_tests %}{% my_test_template_tag %}'
        _check_state(enabled=False)
        old_installed_apps = settings.INSTALLED_APPS
        settings.INSTALLED_APPS = list(old_installed_apps) + [
         b'djblets.template.tests']
        if apps:
            apps.set_installed_apps(settings.INSTALLED_APPS)
        try:
            clear_template_tag_caches()
            _check_state(enabled=True)
        finally:
            settings.INSTALLED_APPS = old_installed_apps
            if apps:
                apps.unset_installed_apps()

        clear_template_tag_caches()
        _check_state(enabled=False)
        Template(b'{% load djblets_js djblets_extensions %}').render(Context({}))

    def test_clear_template_caches(self):
        """Testing clear_template_caches"""
        get_template(b'avatars/avatar.html')
        if engines is not None:
            template_loader = engines.all()[0].engine.template_loaders[0]
        else:
            from django.template.loader import template_source_loaders
            template_loader = template_source_loaders[0]
        self.assertTrue(isinstance(template_loader, CachedLoader))
        if hasattr(template_loader, b'get_template'):
            self.assertNotEqual(template_loader.get_template_cache, {})
        else:
            self.assertNotEqual(template_loader.template_cache, {})
        clear_template_caches()
        if hasattr(template_loader, b'get_template'):
            self.assertEqual(template_loader.get_template_cache, {})
        else:
            self.assertEqual(template_loader.template_cache, {})
        return