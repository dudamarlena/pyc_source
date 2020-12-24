# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-js-reverse/tests/unit_tests.py
# Compiled at: 2018-07-11 18:15:31
from __future__ import unicode_literals
import os, sys, warnings
from string import Template
os.environ[b'DJANGO_SETTINGS_MODULE'] = b'settings'
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.template import RequestContext
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.utils import unittest
from django.utils.encoding import smart_str
from selenium.webdriver.phantomjs.webdriver import WebDriver
from utils import script_prefix
warnings.simplefilter(b'error', DeprecationWarning)

class AbstractJSReverseTestCase(object):
    client = None
    urls = b'tests.test_urls'

    @classmethod
    def setUpClass(cls):
        if hasattr(django, b'setup'):
            django.setup()
        cls.selenium = WebDriver()
        super(AbstractJSReverseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(AbstractJSReverseTestCase, cls).tearDownClass()

    def setUp(self):
        self.client = Client()

    def assertEqualJSUrlEval(self, url_call, expected_url):
        response = self.client.post(b'/jsreverse/')
        self.assertEqual(self.selenium.execute_script(b'%s return %s;' % (smart_str(response.content), url_call)), expected_url)


class JSReverseViewTestCaseMinified(AbstractJSReverseTestCase, TestCase):

    def test_view_no_url_args(self):
        self.assertEqualJSUrlEval(b'Urls.test_no_url_args()', b'/test_no_url_args/')

    def test_view_one_url_arg(self):
        self.assertEqualJSUrlEval(b'Urls.test_one_url_args("arg_one")', b'/test_one_url_args/arg_one/')

    def test_view_two_url_args(self):
        self.assertEqualJSUrlEval(b'Urls.test_two_url_args("arg_one", "arg_two")', b'/test_two_url_args/arg_one-arg_two/')

    def test_view_optional_url_arg(self):
        self.assertEqualJSUrlEval(b'Urls.test_optional_url_arg("arg_two")', b'/test_optional_url_arg/2_arg_two/')
        self.assertEqualJSUrlEval(b'Urls.test_optional_url_arg("arg_one", "arg_two")', b'/test_optional_url_arg/1_arg_one-2_arg_two/')

    def test_unicode_url_name(self):
        self.assertEqualJSUrlEval(b'Urls.test_unicode_url_name()', b'/test_unicode_url_name/')

    @override_settings(JS_REVERSE_JS_VAR_NAME=b'Foo')
    def test_js_var_name_changed_valid(self):
        self.assertEqualJSUrlEval(b'Foo.test_no_url_args()', b'/test_no_url_args/')

    @override_settings(JS_REVERSE_JS_VAR_NAME=b'1test')
    def test_js_var_name_changed_to_invalid(self):
        with self.assertRaises(ImproperlyConfigured):
            self.client.post(b'/jsreverse/')

    def test_namespaces(self):
        self.assertEqualJSUrlEval(b'Urls["ns1:test_two_url_args"]("arg_one", "arg_two")', b'/ns1/test_two_url_args/arg_one-arg_two/')
        self.assertEqualJSUrlEval(b'Urls["ns2:test_two_url_args"]("arg_one", "arg_two")', b'/ns2/test_two_url_args/arg_one-arg_two/')

    def test_namespaces_with_args(self):
        self.assertEqualJSUrlEval(b'Urls["ns_arg:test_two_url_args"]("arg_one", "arg_two", "arg_three")', b'/nsarg_one/test_two_url_args/arg_two-arg_three/')

    def test_namespaces_nested(self):
        self.assertEqualJSUrlEval(b'Urls["nestedns:ns1:test_two_url_args"]("arg_one", "arg_two")', b'/nestedns/ns1/test_two_url_args/arg_one-arg_two/')

    def test_content_type(self):
        response = self.client.post(b'/jsreverse/')
        self.assertEqual(response[b'Content-Type'], b'application/javascript')

    @override_settings(JS_REVERSE_JS_MINIFY=b'invalid')
    def test_js_minfiy_changed_to_invalid(self):
        with self.assertRaises(ImproperlyConfigured):
            self.client.post(b'/jsreverse/')

    def test_namespace_in_urls(self):
        response = self.client.get(b'/jsreverse/')
        self.assertContains(response, b'exclude_namespace', status_code=200)

    @override_settings(JS_REVERSE_EXCLUDE_NAMESPACES=[b'exclude_namespace'])
    def test_namespace_not_in_response(self):
        response = self.client.get(b'/jsreverse/')
        self.assertNotContains(response, b'exclude_namespace', status_code=200)

    def test_script_prefix(self):
        with script_prefix(b'/foobarlala/'):
            self.assertEqualJSUrlEval(b'Urls["nestedns:ns1:test_two_url_args"]("arg_one", "arg_two")', b'/foobarlala/nestedns/ns1/test_two_url_args/arg_one-arg_two/')

    def test_duplicate_name(self):
        self.assertEqualJSUrlEval(b'Urls.test_duplicate_name("arg_one")', b'/test_duplicate_name/arg_one/')
        self.assertEqualJSUrlEval(b'Urls.test_duplicate_name("arg_one", "arg_two")', b'/test_duplicate_name/arg_one-arg_two/')


@override_settings(JS_REVERSE_JS_MINIFY=False)
class JSReverseViewTestCaseNotMinified(JSReverseViewTestCaseMinified):

    def test_minification(self):
        js_not_minified = smart_str(self.client.post(b'/jsreverse/').content)
        with override_settings(JS_REVERSE_JS_MINIFY=True):
            js_minified = smart_str(self.client.post(b'/jsreverse/').content)
            self.assertTrue(len(js_minified) < len(js_not_minified))


class JSReverseViewTestCaseGlobalObjectName(JSReverseViewTestCaseMinified):

    def test_global_object_name_default(self):
        js_content = smart_str(self.client.post(b'/jsreverse/').content)
        self.assertTrue(js_content.startswith(b'this.'))

    @override_settings(JS_REVERSE_JS_GLOBAL_OBJECT_NAME=b'window')
    def test_global_object_name_change(self):
        js_content = smart_str(self.client.post(b'/jsreverse/').content)
        self.assertTrue(js_content.startswith(b'window.'))

    @override_settings(JS_REVERSE_JS_GLOBAL_OBJECT_NAME=b'1test')
    def test_global_object_name_change_invalid_identifier(self):
        with self.assertRaises(ImproperlyConfigured):
            self.client.post(b'/jsreverse/')


class JSReverseStaticFileSaveTest(AbstractJSReverseTestCase, TestCase):

    def test_reverse_js_file_save(self):
        call_command(b'collectstatic_js_reverse')
        path = os.path.join(settings.STATIC_ROOT, b'django_js_reverse', b'js', b'reverse.js')
        f = open(path)
        content1 = f.read()
        if hasattr(content1, b'decode'):
            content1 = content1.decode()
        r2 = self.client.get(b'/jsreverse/')
        content2 = r2.content
        if hasattr(content2, b'decode'):
            content2 = content2.decode()
        self.assertEqual(len(content1), len(content2), b"Static file don't match http response content_1")
        self.assertEqual(content1, content2, b"Static file don't match http response content_2")
        with override_settings(STATIC_ROOT=None):
            with self.assertRaises(ImproperlyConfigured):
                call_command(b'collectstatic_js_reverse')
        return

    def test_script_prefix(self):
        script_prefix = b'/test/foo/bar/'
        with override_settings(JS_REVERSE_SCRIPT_PREFIX=script_prefix):
            self.assertEqualJSUrlEval(b'Urls.test_no_url_args()', (b'{0}test_no_url_args/').format(script_prefix))
        script_prefix = b'/test/foo/bar'
        with override_settings(JS_REVERSE_SCRIPT_PREFIX=script_prefix):
            self.assertEqualJSUrlEval(b'Urls.test_no_url_args()', (b'{0}/test_no_url_args/').format(script_prefix))


class JSReverseTemplateTagTest(AbstractJSReverseTestCase, TestCase):

    def test_tpl_tag_with_request_in_contect(self):
        from django_js_reverse.templatetags.js_reverse import js_reverse_inline
        context_instance = RequestContext(self.client.request)
        Template(b'{%% load %s %%}{%% %s %%}' % (b'js_reverse', js_reverse_inline(context_instance)))

    def test_tpl_tag_without_request_in_contect(self):
        from django_js_reverse.templatetags.js_reverse import js_reverse_inline
        context_instance = RequestContext(None)
        Template(b'{%% load %s %%}{%% %s %%}' % (b'js_reverse', js_reverse_inline(context_instance)))
        return


if __name__ == b'__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), b'..', b'..') + os.sep)
    unittest.main()