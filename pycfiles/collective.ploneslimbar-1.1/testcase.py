# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/ploneseltest/testcase.py
# Compiled at: 2009-10-02 06:04:25
import os, selenium, transaction, Lifetime
from Testing.ZopeTestCase import utils
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase, default_user, default_password
from Products.PloneTestCase.layer import PloneSite as PloneLayer

class SeleniumLayer:
    _selenium = None
    _server = os.environ.get('SELENIUM_HOST', 'localhost')
    _port = os.environ.get('SELENIUM_PORT', '4444')
    _browser = os.environ.get('SELENIUM_BROWSER', '*chrome')
    _site = 'plone'

    @classmethod
    def setUp(cls):
        """Start the Selenium server and the ZServer thread
        """
        (host, port) = utils.startZServer(5)
        url = 'http://%s:%s/%s' % (host, port, cls._site)
        cls._selenium = selenium.selenium(cls._server, cls._port, cls._browser, url)
        cls._selenium.start()

    @classmethod
    def tearDown(cls):
        """Stop the Selenium server and the ZServer thread
        """
        cls._selenium.stop()
        Lifetime.shutdown(0, fast=1)


class SeleniumPloneLayer(PloneLayer, SeleniumLayer):
    pass


class SeleniumTestCase(FunctionalTestCase):
    """Base class for tests that need Selenium support
    """
    layer = SeleniumPloneLayer

    @property
    def selenium(self):
        return self.layer._selenium

    def open(self, path='/', site_name='plone'):
        transaction.commit()
        self.selenium.open('/%s/%s' % (site_name, path))

    def wait(self, timeout='30000'):
        self.selenium.wait_for_page_to_load(timeout)

    def login_user(self, username=default_user, password=default_password):
        self.open('/login')
        self.selenium.type('name=__ac_name', username)
        self.selenium.type('name=__ac_password', password)
        self.selenium.click('submit')
        self.wait()