# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/tests/test_decorators.py
# Compiled at: 2018-03-27 03:51:51
import os
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.conf import settings
from layers import reset_layer_stacks
from layers.monkey import apply_monkey
BASIC_LAYERS_ = {'tree': ['basic', ['web']], 'current': 'basic'}
WEB_LAYERS_ = {'tree': ['basic', ['web']], 'current': 'web'}

class DecoratorFromSettingsTestCase(TestCase):

    def setUp(self):
        super(DecoratorFromSettingsTestCase, self).setUp()
        reset_layer_stacks()
        apply_monkey(force=True)

    @override_settings(LAYERS=BASIC_LAYERS_)
    def test_exclude_from_layers_basic(self):
        url = reverse('normal-view')
        response = self.client.get(url)
        result = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.failUnless('This is a normal view' in result)
        url = reverse('web-only-view')
        response = self.client.get(url)
        result = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.failUnless('is not available for your device' in result)

    @override_settings(LAYERS=WEB_LAYERS_)
    def test_exclude_from_layers_web(self):
        url = reverse('normal-view')
        response = self.client.get(url)
        result = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.failUnless('This is a normal view' in result)
        url = reverse('web-only-view')
        response = self.client.get(url)
        result = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.failUnless('This view is only available for web' in result)


class DecoratorFromRequestTestCase(TestCase):

    def setUp(self):
        super(DecoratorFromRequestTestCase, self).setUp()
        reset_layer_stacks()
        apply_monkey()

    @override_settings(LAYERS=BASIC_LAYERS_)
    def test_exclude_from_layers_basic(self):
        url = reverse('normal-view')
        response = self.client.get(url, **{'X-Django-Layer': 'basic'})
        result = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.failUnless('This is a normal view' in result)
        url = reverse('web-only-view')
        response = self.client.get(url, **{'X-Django-Layer': 'basic'})
        result = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.failUnless('is not available for your device' in result)

    @override_settings(LAYERS=WEB_LAYERS_)
    def test_exclude_from_layers_web(self):
        url = reverse('normal-view')
        response = self.client.get(url, **{'X-Django-Layer': 'web'})
        result = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.failUnless('This is a normal view' in result)
        url = reverse('web-only-view')
        response = self.client.get(url, **{'X-Django-Layer': 'web'})
        result = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.failUnless('This view is only available for web' in result)