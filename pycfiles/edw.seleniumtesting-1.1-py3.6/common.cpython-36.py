# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/seleniumtesting/common.py
# Compiled at: 2018-04-25 11:52:39
# Size of source mod 2**32: 1702 bytes
import os, unittest
from selenium.webdriver.remote.webdriver import WebDriver

class BrowserTestCase(unittest.TestCase):
    __doc__ = ' Custom TestCase wrapper.\n        Needed to support the browser and url paramters.\n    '
    browser = None
    url = None

    def __init__(self, methodName, browser, url, extra_args={}):
        super().__init__(methodName)
        self.browser = browser
        self.url = url
        self.extra_args = extra_args

    @classmethod
    def my_tests(cls):
        """ Helper method used to fetch the available tests for a TestSuite
        """
        return unittest.defaultTestLoader.getTestCaseNames(cls)

    def screenshot(self, suffix: str=''):
        """ Capture a screeenshot.
            Uses `suffix` if given or the current browser url.
        """
        suffix = suffix or self._get_screenshot_suffix()
        name = '{}/screenshot_{}.png'.format(os.getcwd(), suffix)
        self.browser.save_screenshot(name)

    def _get_screenshot_suffix(self) -> str:
        return '_'.join(self.browser.current_url.split('#')[0].split('/')[2:])


class BrowserTestResult(unittest.runner.TextTestResult):
    __doc__ = ' Custom TestResult. Saves screenshots of failed tests.\n    '

    def addFailure(self, test, err):
        test.screenshot()
        super().addFailure(test, err)

    def addError(self, test, err):
        test.screenshot()
        super().addError(test, err)

    def getDescription(self, test):
        """ Include url in the test description.
        """
        text = super().getDescription(test)
        return '[{}] {}'.format(test.url, text)