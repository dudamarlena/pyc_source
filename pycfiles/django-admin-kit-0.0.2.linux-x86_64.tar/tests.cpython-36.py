# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rohan/Django/django-admin-kit/.venv/lib/python3.6/site-packages/tests/test_ping/tests.py
# Compiled at: 2017-11-30 08:43:33
# Size of source mod 2**32: 503 bytes
from django.test.selenium import SeleniumTestCase
from django.contrib.staticfiles.handlers import StaticFilesHandler
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

class TestModule(SeleniumTestCase):
    static_handler = StaticFilesHandler
    browser = 'phantomjs'

    def test_if_ping_exists(self):
        self.selenium.get(self.live_server_url + '/admin_kit/ping')
        self.selenium.find_element_by_xpath('//h1[text()="PONG"]')