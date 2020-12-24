# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_autocomplete/tests/test_it.py
# Compiled at: 2016-11-08 09:30:37
import pickle
from django import forms
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.conf import settings
from simple_autocomplete.widgets import AutoCompleteWidget
from simple_autocomplete.monkey import _simple_autocomplete_queryset_cache
from simple_autocomplete.tests.models import DummyModel

class EditDummyForm(forms.ModelForm):

    class Meta:
        model = DummyModel
        fields = '__all__'


class TestItCase(TestCase):

    def setUp(self):
        self.adam = User.objects.create_user('adam', 'adam@foo.com', 'password')
        self.eve = User.objects.create_user('eve', 'eve@foo.com', 'password')
        self.andre = User.objects.create_user('andré', 'andre@foo.com', 'password')
        self.dummy = DummyModel()
        self.dummy.save()
        self.client = Client()
        self.request = RequestFactory()

    def test_monkey(self):
        form = EditDummyForm(self.request, instance=self.dummy)
        self.failUnless(isinstance(form.fields['user'].widget, AutoCompleteWidget))

    def test_json(self):
        for token, pickled in _simple_autocomplete_queryset_cache.items():
            app_label, model_name, dc = pickle.loads(pickled)
            if app_label == 'auth' and model_name == 'user':
                break

        url = reverse('simple-autocomplete', args=[token])
        response = self.client.get(url, {'q': 'ada'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[[1, "adam"]]')

    def test_unicode(self):
        for token, pickled in _simple_autocomplete_queryset_cache.items():
            app_label, model_name, dc = pickle.loads(pickled)
            if app_label == 'auth' and model_name == 'user':
                break

        url = reverse('simple-autocomplete', args=[token])
        response = self.client.get(url, {'q': 'andr'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[[3, "andr\\u00e9"]]')