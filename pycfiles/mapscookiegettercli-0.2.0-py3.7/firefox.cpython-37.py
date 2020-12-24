# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/mapscookiegettercli/mapscookiegettercli/browsers/firefox.py
# Compiled at: 2019-06-16 09:01:32
# Size of source mod 2**32: 2611 bytes
"""
firefox package

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import logging
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '04-03-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'firefox'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class Firefox:
    __doc__ = 'Bootstraps a firefox selenium driver with the required settings'

    def __new__(cls):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix='bootstrapper')
        logger = logging.getLogger(logger_name)
        logger.info('Starting up firefox driven by selenium')
        driver = webdriver.Firefox(firefox_profile=(webdriver.FirefoxProfile()), executable_path=(GeckoDriverManager().install()))
        logger.info('Deleting all cookies')
        driver.delete_all_cookies()
        logger.info('Returning driver')
        return driver