# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tonio/sources/odooselenium/odooselenium/test.py
# Compiled at: 2016-12-12 05:50:30
"""Testing libraries."""
import unittest
from selenium import webdriver
from odooselenium.ui import OdooUI

class TestCase(unittest.TestCase):

    def setUp(self):
        """Setup Selenium driver, log in."""
        self.configure()
        self.setup_webdriver()
        self.ui = OdooUI(self.webdriver, base_url=self.cfg['url'])
        self.ui.login(self.cfg['username'], self.cfg['password'], self.cfg['dbname'])

    def tearDown(self):
        """Close the webdriver's session."""
        self.webdriver.quit()

    def configure(self, **kwargs):
        """Set :attr:`cfg`."""
        self.cfg = {'url': 'http://localhost:8069', 
           'username': 'admin', 
           'password': 'admin', 
           'dbname': 'test'}
        self.cfg.update(kwargs)

    def setup_webdriver(self):
        """Set :attr:`webdriver`."""
        self.webdriver = webdriver.Chrome()