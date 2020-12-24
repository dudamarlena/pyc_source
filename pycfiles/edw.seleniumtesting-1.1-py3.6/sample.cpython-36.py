# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/seleniumtesting/sample.py
# Compiled at: 2018-04-25 11:52:39
# Size of source mod 2**32: 1280 bytes
import unittest
from edw.seleniumtesting.common import BrowserTestCase

def suite(browser, base_url, extra_args):
    """ Run with `https://google.com/ncr -ea labels search "Google Search"`
    """
    test_suite = unittest.TestSuite()
    for name in GoogleTestCase.my_tests():
        testcase = GoogleTestCase(name, browser, base_url, extra_args)
        test_suite.addTest(testcase)

    return test_suite


class GoogleTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    def test_search_button_exists(self):
        """ 'Google Search' button exists.
        """
        button_label = self.extra_args['labels']['search']
        selector = '//*[@value="{}"]'.format(button_label)
        elements = self.browser.find_elements_by_xpath(selector)
        self.assertGreater(len(elements), 0)