# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/flask/tests/test_foxylib_flask.py
# Compiled at: 2020-01-31 12:33:47
# Size of source mod 2**32: 826 bytes
import logging
from unittest import TestCase
from flask import request
from foxylib.tools.flask.foxylib_flask import FoxylibFlask
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class TestFoxylibFlask(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        app = FoxylibFlask.app()
        with app.test_client() as (client):
            response = client.get('/health_liveness', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = client.get('/health_readiness', follow_redirects=True)
            self.assertEqual(response.status_code, 200)