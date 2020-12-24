# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/app/tests/test_app.py
# Compiled at: 2015-01-01 17:22:32
# Size of source mod 2**32: 4258 bytes
from django.conf import settings
from django.apps import apps as django_app_registry
from django.core.urlresolvers import reverse
from ..core import apps
from .. import menu
from . import base
from kii.tests.test_app import apps as test_apps, models
from ..templatetags import app_tags

class TestApp(base.BaseTestCase):

    def test_can_get_app(self):
        app = apps.get('test_app')
        self.assertEqual(isinstance(app, test_apps.App), True)

    def test_can_get_all_apps(self):
        all_apps = list(apps.all())
        django_apps = list(django_app_registry.get_app_configs())
        self.assertEqual(django_apps, all_apps)

    def test_can_get_kii_app(self):
        kii_apps = apps.kii_apps()
        self.assertEqual(len(kii_apps), len(settings.KII_APPS + settings.TEST_APPS))
        for app in kii_apps:
            self.assertIn(app.name, settings.KII_APPS + settings.TEST_APPS)

    def test_kii_apps_are_registered(self):
        for a in settings.KII_APPS:
            self.assertEqual(True, django_app_registry.is_installed(a))

    def test_kii_app_installed_property(self):
        for app in apps.kii_apps():
            self.assertEqual(app.installed, True)

    def test_can_get_app_public_models(self):
        public_models = apps.get('test_app').public_models()
        self.assertEqual(public_models, [models.PublicModel])

    def test_can_gather_urls_for_kii_apps(self):
        reverse('kii:test_app:index')
        reverse('kii:test_app1:some_view')
        reverse('kii:test_app2:third_view')

    def test_gathered_urls_also_accept_username_kwarg(self):
        reverse('kii:user_area:test_app:index', kwargs={'username': 'test0'})
        reverse('kii:user_area:test_app1:some_view', kwargs={'username': 'test1'})
        reverse('kii:user_area:test_app2:third_view', kwargs={'username': 'test2'})

    def test_app_templates_inherit_from_page_template(self):
        response = self.client.get(reverse('kii:test_app:home'))
        self.assertTemplateUsed(response, 'app/app_page.html')
        self.assertTemplateUsed(response, 'glue/base.html')

    def test_app_pages_title_contains_app_verbose_name(self):
        response = self.client.get(reverse('kii:test_app:home'))
        parsed = self.parse_html(response.content)
        self.assertIn('Test app', parsed.title.string)

    def test_app_can_register_menu_items(self):
        self.assertEqual(apps.get('test_app').menu.url(), '/kii/test_app/hello')
        self.assertEqual(apps.get('test_app').menu.label, 'Test App Index')
        self.assertEqual(apps.get('test_app').menu.title, 'Click to return home')

    def test_menu_item_children_are_ordered_by_weight(self):
        self.assertEqual(apps.get('test_app').menu.children[0].url(), '/kii/test_app/hello/first')
        self.assertEqual(apps.get('test_app').menu.children[1].url(), '/kii/test_app/hello/second')
        self.assertEqual(apps.get('test_app').menu.children[2].url(), '/kii/test_app/hello/third')

    def test_can_have_menu_node_without_reversing_url(self):
        m = menu.MenuNode(route='http://example.com', reverse=False)
        self.assertEqual(m.url(), 'http://example.com')

    def test_menu_item_with_user_url(self):
        m = menu.MenuNode(route='kii:user_area:test_app:user', reverse=True, reverse_kwargs=[
         'username'])
        self.assertEqual(m.url(username='test0'), '/kii/u/test0/test_app/hello/user')

    def test_menu_url_template_tag(self):
        m = menu.MenuNode(route='kii:user_area:test_app:user', reverse=True, reverse_kwargs=[
         'username'])
        url = app_tags.node_url(m, username='test0')
        self.assertEqual(url, '/kii/u/test0/test_app/hello/user')

    def test_app_view_suffix_with_app_name(self):
        url = reverse('kii:test_app:home')
        response = self.client.get(url)
        self.assertEqual(response.context['full_title'].endswith('Test app'), True)