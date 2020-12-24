# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/test/selenium.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import sys, unittest
from contextlib import contextmanager
from django.test import LiveServerTestCase, tag
from django.utils.module_loading import import_string
from django.utils.six import with_metaclass
from django.utils.text import capfirst

class SeleniumTestCaseBase(type(LiveServerTestCase)):
    browsers = []
    browser = None

    def __new__(cls, name, bases, attrs):
        """
        Dynamically create new classes and add them to the test module when
        multiple browsers specs are provided (e.g. --selenium=firefox,chrome).
        """
        test_class = super(SeleniumTestCaseBase, cls).__new__(cls, name, bases, attrs)
        if test_class.browser or not any(name.startswith(b'test') and callable(value) for name, value in attrs.items()):
            return test_class
        if test_class.browsers:
            first_browser = test_class.browsers[0]
            test_class.browser = first_browser
            module = sys.modules[test_class.__module__]
            for browser in test_class.browsers[1:]:
                browser_test_class = cls.__new__(cls, str(b'%s%s' % (capfirst(browser), name)), (
                 test_class,), {b'browser': browser, b'__module__': test_class.__module__})
                setattr(module, browser_test_class.__name__, browser_test_class)

            return test_class
        return unittest.skip(b'No browsers specified.')(test_class)

    @classmethod
    def import_webdriver(cls, browser):
        return import_string(b'selenium.webdriver.%s.webdriver.WebDriver' % browser)

    def create_webdriver(self):
        return self.import_webdriver(self.browser)()


@tag(b'selenium')
class SeleniumTestCase(with_metaclass(SeleniumTestCaseBase, LiveServerTestCase)):
    implicit_wait = 10

    @classmethod
    def setUpClass(cls):
        cls.selenium = cls.create_webdriver()
        cls.selenium.implicitly_wait(cls.implicit_wait)
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def _tearDownClassInternal(cls):
        if hasattr(cls, b'selenium'):
            cls.selenium.quit()
        super(SeleniumTestCase, cls)._tearDownClassInternal()

    @contextmanager
    def disable_implicit_wait(self):
        """Context manager that disables the default implicit wait."""
        self.selenium.implicitly_wait(0)
        try:
            yield
        finally:
            self.selenium.implicitly_wait(self.implicit_wait)