# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/auth/auth0/tests/test_foxylib_auth0.py
# Compiled at: 2020-01-21 01:42:50
# Size of source mod 2**32: 1919 bytes
import logging
from unittest import TestCase
import requests
from flask import Response
from foxylib.tools.auth.auth0.foxylib_auth0 import FoxylibAuth0
from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.flask.foxylib_flask import FoxylibFlask
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.url.url_tool import URLTool

class TestFoxylibAuth0(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        app, auth0 = FoxylibAuth0.app_auth0()
        c = app.test_client()
        response_login = c.get('/auth0/login/', follow_redirects=False)
        self.assertEqual(response_login.status_code, 302)
        url_auth0 = response_login.location
        self.assertTrue(url_auth0.startswith('https://dev-8gnjw0rn.auth0.com/authorize'))
        h_next = URLTool.url2h_query(url_auth0)
        redirect_uri = l_singleton2obj(h_next.get('redirect_uri'))
        self.assertEqual(redirect_uri, 'http://localhost:5000/auth0/callback/')
        response_auth0 = requests.get(url_auth0)
        logger.debug({'response_auth0': response_auth0})
        self.assertEqual(response_auth0.status_code, 200)
        self.assertIn('Log in to foxylib', response_auth0.text)
        self.assertIn('Log in to dev-8gnjw0rn to continue to foxylib', response_auth0.text)