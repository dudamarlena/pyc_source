# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/tests/test_01_core.py
# Compiled at: 2020-04-15 11:39:00
# Size of source mod 2**32: 8874 bytes
from unittest import SkipTest
import django
from django.core import management
from django.test import TestCase, override_settings
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from django_selenium_test import PageElement, SeleniumTestCase

class DjangoSeleniumCleanTestCase(SeleniumTestCase):
    heading_earth = PageElement(By.ID, 'earth')
    heading_world = PageElement(By.ID, 'world')
    user_info = PageElement(By.ID, 'user')
    button_toggle_heading = PageElement(By.ID, 'toggle-heading')
    button_open_window = PageElement(By.ID, 'open-window')
    button_toggle_element = PageElement(By.ID, 'toggle-element')
    button_toggle_message = PageElement(By.ID, 'toggle-message')
    togglable = PageElement(By.ID, 'togglable')
    message = PageElement(By.ID, 'message')

    def _load_core_page(self):
        self.selenium.get(self.live_server_url + '/core')

    def test_toggle(self):
        self._load_core_page()
        self.assertTrue(self.heading_earth.is_displayed())
        self.assertFalse(self.heading_world.is_displayed())
        self.button_toggle_heading.click()
        self.heading_world.wait_until_is_displayed()
        self.assertFalse(self.heading_earth.is_displayed())
        self.assertTrue(self.heading_world.is_displayed())
        self.button_toggle_heading.click()
        self.heading_earth.wait_until_is_displayed()
        self.assertTrue(self.heading_earth.is_displayed())
        self.assertFalse(self.heading_world.is_displayed())

    def test_login(self):
        from django.contrib.auth.hashers import make_password
        from django.contrib.auth.models import User
        cap = self.selenium.capabilities
        if cap['browserName'] == 'phantomjs':
            if cap['version'] == '2.1.1':
                raise SkipTest('https://github.com/ariya/phantomjs/issues/14228')
        alice = User.objects.create(username='alice',
          password=(make_password('topsecret')),
          is_active=True)
        self._load_core_page()
        self.user_info.wait_until_is_displayed()
        self.assertEqual(self.user_info.text, 'No user is logged on.')
        r = self.selenium.login(username='alice', password='topsecret')
        self.assertTrue(r)
        self._load_core_page()
        self.user_info.wait_until_is_displayed()
        self.assertEqual(self.user_info.text, 'The logged on user is alice.')
        self.selenium.logout()
        self._load_core_page()
        self.user_info.wait_until_is_displayed()
        self.assertEqual(self.user_info.text, 'No user is logged on.')
        r = self.selenium.force_login(alice, base_url=(self.live_server_url))
        self.assertIsNone(r)
        self._load_core_page()
        self.user_info.wait_until_is_displayed()
        self.assertEqual(self.user_info.text, 'The logged on user is alice.')
        self.selenium.logout()
        self._load_core_page()
        self.user_info.wait_until_is_displayed()
        self.assertEqual(self.user_info.text, 'No user is logged on.')

    def test_wait_until_n_windows(self):
        self._load_core_page()
        with self.assertRaises(AssertionError):
            self.selenium.wait_until_n_windows(n=2, timeout=1)
        self.button_open_window.click()
        self.selenium.wait_until_n_windows(n=2, timeout=1)
        self.selenium.switch_to_window(self.selenium.window_handles[1])
        self.selenium.close()
        self.selenium.switch_to_window(self.selenium.window_handles[0])

    def test_exists(self):
        self._load_core_page()
        self.togglable.wait_until_not_exists()
        self.assertFalse(self.togglable.exists())
        with self.assertRaises(TimeoutException):
            self.togglable.wait_until_exists(timeout=1)
        self.button_toggle_element.click()
        self.togglable.wait_until_exists()
        self.assertTrue(self.togglable.exists())
        with self.assertRaises(TimeoutException):
            self.togglable.wait_until_not_exists(timeout=1)
        self.button_toggle_element.click()
        self.togglable.wait_until_not_exists()
        self.assertFalse(self.togglable.exists())
        with self.assertRaises(TimeoutException):
            self.togglable.wait_until_exists(timeout=1)

    def test_is_displayed(self):
        self._load_core_page()
        self.heading_world.wait_until_exists()
        self.heading_world.wait_until_not_displayed()
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_not_exists(timeout=1)
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_is_displayed(timeout=1)
        self.assertTrue(self.heading_world.exists())
        self.assertFalse(self.heading_world.is_displayed())
        self.button_toggle_heading.click()
        self.heading_world.wait_until_exists()
        self.heading_world.wait_until_is_displayed()
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_not_exists(timeout=1)
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_not_displayed(timeout=1)
        self.assertTrue(self.heading_world.exists())
        self.assertTrue(self.heading_world.is_displayed())
        self.button_toggle_heading.click()
        self.heading_world.wait_until_exists()
        self.heading_world.wait_until_not_displayed()
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_not_exists(timeout=1)
        with self.assertRaises(TimeoutException):
            self.heading_world.wait_until_is_displayed(timeout=1)
        self.assertTrue(self.heading_world.exists())
        self.assertFalse(self.heading_world.is_displayed())

    def test_contains(self):
        self._load_core_page()
        self.message.wait_until_contains('earth')
        self.message.wait_until_not_contains('world')
        with self.assertRaises(TimeoutException):
            self.message.wait_until_contains('world', timeout=1)
        with self.assertRaises(TimeoutException):
            self.message.wait_until_not_contains('earth', timeout=1)
        self.assertTrue('earth' in self.message.text)
        self.assertFalse('world' in self.message.text)
        self.button_toggle_message.click()
        self.message.wait_until_contains('world')
        self.message.wait_until_not_contains('earth')
        with self.assertRaises(TimeoutException):
            self.message.wait_until_contains('earth', timeout=1)
        with self.assertRaises(TimeoutException):
            self.message.wait_until_not_contains('world', timeout=1)
        self.assertTrue('world' in self.message.text)
        self.assertFalse('earth' in self.message.text)


@override_settings(SELENIUM_WEBDRIVERS=False)
class DjangoSeleniumCleanSkipTestCase(TestCase):

    def test_skip_test(self):

        class SkippedTestCase(SeleniumTestCase):

            def runTest(self):
                pass

        instance = SkippedTestCase()
        instance()