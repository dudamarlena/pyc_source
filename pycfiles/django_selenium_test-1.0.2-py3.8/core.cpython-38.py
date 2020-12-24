# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/django_selenium_test/core.py
# Compiled at: 2020-04-15 11:39:00
# Size of source mod 2**32: 10068 bytes
from __future__ import absolute_import, annotations
import os, signal, time
from importlib import import_module
from typing import TYPE_CHECKING
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.http import HttpRequest
import selenium.webdriver.support as EC
from selenium.webdriver.support.ui import WebDriverWait
if TYPE_CHECKING:
    from typing import Optional, Any
    from selenium.webdriver.remote.webdriver import WebDriver
    from django.contrib.auth.models import AbstractUser

class SeleniumWrapper(object):
    _instance = None
    driver: 'WebDriver'

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = (super().__new__)(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> 'None':
        SELENIUM_WEBDRIVERS = getattr(settings, 'SELENIUM_WEBDRIVERS', {})
        if not SELENIUM_WEBDRIVERS:
            return
        driver_id = os.environ.get('SELENIUM_WEBDRIVER', 'default')
        driver = SELENIUM_WEBDRIVERS[driver_id]
        callable = driver['callable']
        args = driver['args']
        kwargs = driver['kwargs']
        self.driver = callable(*args, **kwargs)

    def __getattr__(self, name: 'str') -> 'Any':
        return getattr(self.driver, name)

    def __setattr__(self, name, value):
        if name == 'driver':
            super(SeleniumWrapper, self).__setattr__(name, value)
        else:
            setattr(self.driver, name, value)

    def __bool__(self) -> 'bool':
        return bool(self.driver)

    __nonzero__ = __bool__

    def login(self, **credentials: 'Any') -> 'bool':
        """
        Sets selenium to appear as if a user has successfully signed in.

        Returns True if signin is possible; False if the provided
        credentials are incorrect, or the user is inactive, or if the
        sessions framework is not available.

        The code is based on django.test.client.Client.login.
        """
        from django.contrib.auth import authenticate
        user = authenticate(**credentials)
        if user:
            if user.is_active:
                if 'django.contrib.sessions' in settings.INSTALLED_APPS:
                    self._login(user)
                    return True
        return False

    def force_login(self, user: 'AbstractUser', base_url: 'str') -> 'None':
        """
        Sets selenium to appear as if a user has successfully signed in.

        The user will have its backend attribute set to the value of the
        backend argument (which should be a dotted Python path string),
        or to settings.AUTHENTICATION_BACKENDS[0] if a value isn't
        provided. The authenticate() function called by login() normally
        annotates the user like this.

        The code is based on https://github.com/feffe/django-selenium-login/blob/master/seleniumlogin/__init__.py. 
        """
        from django.conf import settings
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        selenium_login_start_page = getattr(settings, 'SELENIUM_LOGIN_START_PAGE', '/page_404/')
        self.driver.get('{}{}'.format(base_url, selenium_login_start_page))
        session = SessionStore()
        session[SESSION_KEY] = user.id
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()
        cookie = {'name':settings.SESSION_COOKIE_NAME, 
         'value':session.session_key, 
         'path':'/'}
        self.driver.add_cookie(cookie)
        self.driver.refresh()

    def _login(self, user: 'AbstractUser', backend: 'Optional[str]'=None) -> 'None':
        from django.contrib.auth import login
        engine = import_module(settings.SESSION_ENGINE)
        request = HttpRequest()
        request.session = engine.SessionStore()
        login(request, user, backend)
        request.session.save()
        cookie_data = {'name':settings.SESSION_COOKIE_NAME, 
         'value':request.session.session_key, 
         'max-age':None, 
         'path':'/', 
         'secure':settings.SESSION_COOKIE_SECURE or False, 
         'expires':None}
        self.add_cookie(cookie_data)
        return True

    def logout(self) -> 'None':
        """
        Removes the authenticated user's cookies and session object.

        Causes the authenticated user to be logged out.
        """
        session = import_module(settings.SESSION_ENGINE).SessionStore()
        session_cookie = self.get_cookie(settings.SESSION_COOKIE_NAME)
        if session_cookie:
            session.delete(session_key=(session_cookie['value']))
            self.delete_cookie(settings.SESSION_COOKIE_NAME)

    def wait_until_n_windows(self, n: 'int', timeout: 'int'=2) -> 'None':
        for i in range(timeout * 10):
            if len(self.window_handles) == n:
                return
                time.sleep(0.1)
        else:
            raise AssertionError('Timeout while waiting for {0} windows'.format(n))

    def quit(self) -> 'None':
        if self.driver.capabilities['browserName'] == 'phantomjs':
            self.driver.service.process.send_signal(signal.SIGTERM)
        else:
            self.driver.quit()


class SeleniumTestCase(StaticLiveServerTestCase):
    selenium: 'SeleniumWrapper'

    @classmethod
    def setUpClass(cls):
        super(SeleniumTestCase, cls).setUpClass()
        cls.selenium = SeleniumWrapper()
        PageElement.selenium = cls.selenium
        cls.selenium.live_server_url = 'http://%s:%s' % (
         cls.server_thread.host,
         cls.server_thread.port)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        PageElement.selenium = None
        super().tearDownClass()

    def __call__(self, result=None):
        if hasattr(self, 'selenium'):
            for width in getattr(settings, 'SELENIUM_WIDTHS', [1024]):
                self.selenium.set_window_size(width, 1024)

        return super().__call__(result)


class PageElement(object):
    selenium = None
    selenium: 'Optional[WebDriver]'

    def __init__(self, *args: 'Any') -> 'None':
        if len(args) == 2:
            self.locator = args

    def wait_until_exists(self, timeout: 'int'=10) -> 'None':
        WebDriverWait(self.selenium, timeout).until(EC.presence_of_element_located(self.locator))

    def wait_until_not_exists(self, timeout: 'int'=10) -> 'None':
        WebDriverWait(self.selenium, timeout).until_not(EC.presence_of_element_located(self.locator))

    def wait_until_is_displayed(self, timeout: 'int'=10) -> 'None':
        WebDriverWait(self.selenium, timeout).until(EC.visibility_of_element_located(self.locator))

    def wait_until_not_displayed(self, timeout: 'int'=10) -> 'None':
        WebDriverWait(self.selenium, timeout).until_not(EC.visibility_of_element_located(self.locator))

    def wait_until_contains(self, text: 'str', timeout: 'int'=10) -> 'None':
        WebDriverWait(self.selenium, timeout).until(EC.text_to_be_present_in_element(self.locator, text))

    def wait_until_not_contains(self, text: 'str', timeout: 'int'=10) -> 'None':
        WebDriverWait(self.selenium, timeout).until_not(EC.text_to_be_present_in_element(self.locator, text))

    def wait_until_is_clickable(self, timeout: 'int'=10) -> 'None':
        WebDriverWait(self.selenium, timeout).until(EC.element_to_be_clickable(self.locator))

    def exists(self) -> 'bool':
        return len((self.selenium.find_elements)(*self.locator)) > 0

    def __getattr__(self, name: 'str') -> 'Any':
        return getattr((self.selenium.find_element)(*self.locator), name)