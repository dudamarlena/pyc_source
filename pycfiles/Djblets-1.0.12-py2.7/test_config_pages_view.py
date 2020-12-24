# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/configforms/tests/test_config_pages_view.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.configforms.views.ConfigPagesView."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.http import Http404
from django.test.client import RequestFactory
from django.utils import six
from djblets.configforms.forms import ConfigPageForm
from djblets.configforms.pages import ConfigPage
from djblets.configforms.views import ConfigPagesView
from djblets.testing.testcases import TestCase

class TestForm1(ConfigPageForm):
    form_id = b'my-form-1'
    form_title = b'Form 1'

    def save(self):
        pass


class TestForm2(ConfigPageForm):
    form_id = b'my-form-2'
    form_title = b'Form 2'


class TestForm3(ConfigPageForm):
    form_id = b'my-form-3'
    form_title = b'Form 3'

    def is_visible(self):
        return False


class TestPage1(ConfigPage):
    page_id = b'my-page-1'
    form_classes = [TestForm1]


class TestPage2(ConfigPage):
    page_id = b'my-page-2'
    form_classes = [TestForm2]


class TestPage3(ConfigPage):
    page_id = b'my-page-3'
    form_classes = [TestForm3]


class MyConfigPagesView(ConfigPagesView):
    title = b'My Page Title'
    nav_title = b'My Nav Entry'
    page_classes = [TestPage1, TestPage2, TestPage3]
    css_bundle_names = [
     b'my-css-bundle']
    js_bundle_names = [b'my-js-bundle']
    js_model_class = b'MyModel'
    js_view_class = b'MyView'

    def get_js_model_data(self):
        return {b'my-attr': b'value'}

    def get_js_view_data(self):
        return {b'my-option': b'value'}


class ConfigPagesViewTests(TestCase):
    """Unit tests for djblets.configforms.views.ConfigPagesView."""

    def test_dispatch_initial_state(self):
        """Testing ConfigPagesView.dispatch initial state"""
        request = RequestFactory().request()
        request.user = User.objects.create(username=b'test-user')
        view = MyConfigPagesView()
        view.request = request
        response = view.dispatch(view.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(view.pages), 2)
        self.assertIsInstance(view.pages[0], TestPage1)
        self.assertIsInstance(view.pages[1], TestPage2)
        self.assertEqual(set(six.iterkeys(view.forms)), {
         b'my-form-1', b'my-form-2'})

    def test_get_context_data(self):
        """Testing ConfigPagesView.get_context_data"""
        request = RequestFactory().request()
        request.user = User.objects.create(username=b'test-user')
        view = MyConfigPagesView()
        view.request = request
        view.dispatch(view.request)
        self.assertEqual(view.get_context_data(), {b'base_template_name': b'base.html', 
           b'page_title': b'My Page Title', 
           b'nav_title': b'My Nav Entry', 
           b'pages_id': b'config_pages', 
           b'pages': view.pages, 
           b'css_bundle_names': [
                               b'my-css-bundle'], 
           b'js_bundle_names': [
                              b'my-js-bundle'], 
           b'js_model_class': b'MyModel', 
           b'js_view_class': b'MyView', 
           b'js_model_data': {b'my-attr': b'value'}, 
           b'js_view_data': {b'my-option': b'value'}, 
           b'forms': list(six.itervalues(view.forms)), 
           b'render_sidebar': True})

    def test_post_without_form_target(self):
        """Testing ConfigPagesView.dispatch with POST and no form_target"""
        request = RequestFactory().post(b'/config/')
        request.user = User.objects.create(username=b'test-user')
        request._dont_enforce_csrf_checks = True
        view = MyConfigPagesView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_post_with_invalid_form_target(self):
        """Testing ConfigPagesView.dispatch with POST and invalid form_target
        """
        request = RequestFactory().post(b'/config/', {b'form_target': b'bad'})
        request.user = User.objects.create(username=b'test-user')
        request._dont_enforce_csrf_checks = True
        view = MyConfigPagesView.as_view()
        with self.assertRaises(Http404):
            view(request)

    def test_post_with_success(self):
        """Testing ConfigPagesView.dispatch with POST and success"""
        request = RequestFactory().post(b'/config/', {b'form_target': b'my-form-1'})
        request.user = User.objects.create(username=b'test-user')
        request._dont_enforce_csrf_checks = True
        view = MyConfigPagesView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response[b'Location'], b'/config/')