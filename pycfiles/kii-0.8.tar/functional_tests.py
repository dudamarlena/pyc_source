# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/glue/tests/functional_tests.py
# Compiled at: 2015-01-17 16:40:50
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django_dynamic_fixture import G
import time, unittest
from kii.app.core import apps as app_manager
from kii.stream import models as stream_models
from kii.classify.models import Tag
from . import SeleniumTestCase

class GlueTest(SeleniumTestCase):

    @unittest.skip('too early for functional tests')
    def test_user_can_display_home_page_and_login(self):
        user = G(get_user_model(), username='harold')
        user.set_password('test')
        user.save()
        stream = stream_models.Stream.objects.get(owner=user, title=user.username)
        for i in range(0, 5):
            G(stream_models.StreamItem, root=stream)

        for i in range(0, 5):
            G(Tag, owner=user)

        self.browser.get(self.url(reverse('kii:glue:home')))
        self.assertIn('Welcome', self.browser.title)
        self.browser.find_element_by_css_selector('nav .login').click()
        login_form = self.browser.find_element_by_css_selector('form#login')
        username_input = login_form.find_element_by_css_selector('input[type="text"]')
        password_input = login_form.find_element_by_css_selector('input[name="password"]')
        username_input.send_keys('harold')
        password_input.send_keys('test')
        password_input.send_keys(self.keys.RETURN)
        result_popup = self.browser.find_element_by_css_selector('.messages .success')
        self.assertIn('user.login.success', result_popup.text)
        self.assertEqual(self.browser.current_url, self.url(reverse('kii:stream:index')))
        tags = self.browser.find_elements_by_css_selector('.widget.tags > ul > .tag')
        self.assertEqual(len(tags), Tag.objects.filter(owner=user).count())
        expected_items = stream.children.all().order_by('-publication_date')
        items = self.browser.find_elements_by_css_selector('.stream-items > article')
        self.assertEqual(len(items), len(expected_items))
        for i, item in enumerate(items):
            title = item.find_element_by_css_selector('h2.title')
            self.assertEqual(title.text, expected_items[i].title)

        apps = self.browser.find_elements_by_css_selector('.apps > li > a')
        expected_apps = app_manager.filter(user_access=True)
        self.assertEqual(len(apps), len(expected_apps))
        for i, app in enumerate(apps):
            self.assertEqual(app.text, expected_apps[i].verbose_name)

        apps[0].click()
        self.assertEqual(self.browser.current_url, self.url(reverse(('kii:{0}:index').format(expected_apps[0].label))))