# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/source/ambition-edc/venv/lib/python3.7/site-packages/edc_selenium/mixins/selenium_utils_mixin.py
# Compiled at: 2019-01-21 20:09:21
# Size of source mod 2**32: 682 bytes
from selenium.webdriver.common.by import By
import selenium.webdriver.support as EC
from selenium.webdriver.support.ui import WebDriverWait

class SeleniumUtilsMixin:

    def wait_for(self, text, by=None, timeout=None):
        """Explicit wait.

        Default is by partial link text
        """
        timeout = timeout or 20
        by = by or By.PARTIAL_LINK_TEXT
        element = WebDriverWait(self.selenium, timeout).until(EC.presence_of_element_located((by, text)))
        return element

    def wait_for_edc(self):
        WebDriverWait(self.selenium, 20).until(EC.presence_of_element_located((By.ID, 'edc-body')))