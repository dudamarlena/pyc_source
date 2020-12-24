# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/djangoflash/tests/testproj/app/tests.py
# Compiled at: 2011-02-12 22:31:36
"""Integration test cases.
"""
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.test import TestCase
from djangoflash.context_processors import CONTEXT_VAR
from djangoflash.middleware import FlashScope
from testproj.app import views

class IntegrationTestCase(TestCase):
    """Test the middleware and the context processors working within a real
    Django application.
    """

    def _flash(self):
        """Shortcut to get the flash from the view context.
        """
        return self.response.context[CONTEXT_VAR]

    def test_default_lifecycle(self):
        """Integration: a value should be automatically removed from the flash.
        """
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_value_in_template(self):
        """Integration: a value should be accessible by the templating system.
        """

        def _assert_content(content, exists=True):
            if exists:
                matcher = self.assertTrue
            else:
                matcher = self.assertFalse
            matcher(self.response.content.find(content) > 0)

        self.response = self.client.get(reverse(views.set_flash_var))
        _assert_content('Flash context: Message', exists=True)
        self.response = self.client.get(reverse(views.render_template))
        _assert_content('Flash context: Message', exists=True)
        self.response = self.client.get(reverse(views.render_template))
        _assert_content('Flash context: Message', exists=False)

    def test_keep_lifecycle(self):
        """Integration: a value shouldn't be removed from the flash when it is kept.
        """
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.keep_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_keep_decorator(self):
        """Integration: keep_messages decorator should behave exactly like keep.
        """
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.keep_var_decorator))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_now_lifecycle(self):
        """Integration: an immediate value shouldn't survive the next request.
        """
        self.response = self.client.get(reverse(views.set_now_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_discard_lifecycle(self):
        """Integration: a discarded value shouldn't survive to the next request.
        """
        self.response = self.client.get(reverse(views.discard_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_multiple_variables_lifecycle(self):
        """Integration: the flash should control several values independently.
        """
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.set_another_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.assertEqual('Another message', self._flash()['anotherMessage'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())
        self.assertEqual('Another message', self._flash()['anotherMessage'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())
        self.assertFalse('anotherMessage' in self._flash())

    def test_remove_flash(self):
        """Integration: an empty flash should be provided when none is available.
        """
        self.response = self.client.get(reverse(views.remove_flash))
        self.assertTrue(isinstance(self._flash(), FlashScope))

    def test_replace_flash_with_invalid_object(self):
        """Integration: an exception should be raised when exposing an invalid object as being the flash.
        """
        self.assertRaises(SuspiciousOperation, self.client.get, reverse(views.replace_flash))

    def test_request_to_serve_view_without_ignore(self):
        """Integration: request to static resources should trigger the flash update.
        """
        settings.FLASH_IGNORE_MEDIA = False
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(settings.MEDIA_URL + 'test.css')
        self.assertEqual(200, self.response.status_code)
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_request_to_serve_view_with_ignore(self):
        """Integration: request to static resources should not trigger the flash update, if properly configured.
        """
        settings.FLASH_IGNORE_MEDIA = True
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(settings.MEDIA_URL + 'test.css')
        self.assertEqual(200, self.response.status_code)
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_request_to_serve_view_with_default_value(self):
        """Integration: request to static resources should not trigger the flash update in debug mode.
        """
        if hasattr(settings, 'FLASH_IGNORE_MEDIA'):
            del settings.FLASH_IGNORE_MEDIA
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(settings.MEDIA_URL + 'test.css')
        self.assertEqual(200, self.response.status_code)
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())

    def test_flash_with_common_middleware_and_missing_trailing_slash(self):
        """Integration: missing trailing slash in URL should not affect the flash lifecycle when using the CommonMiddleware.
        """
        self.response = self.client.get(reverse(views.set_flash_var))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get('/default')
        self.response = self.client.get(reverse(views.render_template))
        self.assertEqual('Message', self._flash()['message'])
        self.response = self.client.get(reverse(views.render_template))
        self.assertFalse('message' in self._flash())