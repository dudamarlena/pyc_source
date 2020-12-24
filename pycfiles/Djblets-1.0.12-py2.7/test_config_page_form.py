# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/configforms/tests/test_config_page_form.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.configforms.forms.ConfigPageForm."""
from __future__ import unicode_literals
import warnings
from django import forms
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.utils import six
from djblets.configforms.forms import ConfigPageForm
from djblets.configforms.pages import ConfigPage
from djblets.configforms.views import ConfigPagesView
from djblets.deprecation import RemovedInDjblets20Warning
from djblets.testing.testcases import TestCase

class TestForm(ConfigPageForm):
    form_id = b'my-form'
    field1 = forms.CharField(label=b'Field 1', required=False)
    field2 = forms.CharField(label=b'Field 2', required=False)


class TestPage(ConfigPage):
    page_id = b'my-page'
    form_classes = [TestForm]


class ConfigPageFormTests(TestCase):
    """Unit tests for djblets.configforms.forms.ConfigPageForm."""

    def setUp(self):
        super(ConfigPageFormTests, self).setUp()
        request = RequestFactory().request()
        user = User.objects.create_user(username=b'test-user', password=b'test-user')
        page = TestPage(ConfigPagesView, request, user)
        self.form = TestForm(page, request, user)

    def test_initial_state(self):
        """Testing ConfigPageForm initial state"""
        self.assertEqual(self.form.fields[b'form_target'].initial, b'my-form')

    def test_profile(self):
        """Testing ConfigPageForm.profile raises a deprecation warning"""
        with warnings.catch_warnings(record=True) as (w):
            try:
                self.form.profile
            except Exception:
                pass

        message = w[0].message
        self.assertIsInstance(message, RemovedInDjblets20Warning)
        self.assertEqual(six.text_type(message), b'ConfigFormPage.profile is deprecated. Update your code to fetch the profile manually instead.')

    def test_set_initial(self):
        """Testing ConfigPageForm.set_initial"""
        self.form.set_initial({b'field1': b'foo', 
           b'field2': b'bar'})
        self.assertEqual(self.form.fields[b'field1'].initial, b'foo')
        self.assertEqual(self.form.fields[b'field2'].initial, b'bar')

    def test_render(self):
        """Testing ConfigPageForm.render"""
        rendered = self.form.render()
        self.assertHTMLEqual(b'<input id="id_form_target" name="form_target" type="hidden" value="my-form"><div class="fields-row field-field1" id="row-field1"> <div class="field">  <label for="id_field1">Field 1:</label>  <input id="id_field1" name="field1" type="text"> </div></div><div class="fields-row field-field2" id="row-field2"> <div class="field">  <label for="id_field2">Field 2:</label>  <input id="id_field2" name="field2" type="text"> </div></div><input type="submit" class="btn" value="Save">', rendered)