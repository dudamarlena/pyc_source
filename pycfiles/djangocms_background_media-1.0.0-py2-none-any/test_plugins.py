# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/life-website-env/life-website/website/website/apps/djangocms_background_media/tests/test_plugins.py
# Compiled at: 2016-06-23 11:13:17
from __future__ import unicode_literals
from django.test import TestCase
from cms.api import add_plugin
from cms.models import Placeholder
from ..cms_plugins import BackgroundMediaPlugin

class BackgroundMediaPluginTests(TestCase):

    def test_plugin_context(self):
        placeholder = Placeholder.objects.create(slot=b'test')
        model_instance = add_plugin(placeholder, BackgroundMediaPlugin, b'en')
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        self.assertIn(b'instance', context)
        return

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot=b'test')
        model_instance = add_plugin(placeholder, BackgroundMediaPlugin, b'en')
        html = model_instance.render_plugin({})
        self.assertTrue(html.find(b'class="djangocms-bg-media"') > -1)