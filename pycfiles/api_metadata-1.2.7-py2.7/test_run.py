# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/tests/test_run.py
# Compiled at: 2017-11-27 05:07:42
from mock import patch
from api_metadata.run import app_factory, debug, wsgi
from flask import Flask
from ocs.api.logger import FlaskExceptHook
from ocs.conf import Configuration
from ocs.unittest import MockTestCase

class TestRun(MockTestCase):
    patches = [
     patch('ocs.api.logger.Sentry')]

    def setUp(self):
        super(TestRun, self).setUp()
        Configuration.load_from_dict({'sentry': {'dsn': 'udp://user:token@example.org:9000/42'}}, FlaskExceptHook.configuration_name)

    def test_run_wsgi(self):
        with patch.object(Flask, 'wsgi_app', autospec=True) as (mock_run):
            wsgi([], None)
        self.assertEqual(1, len(mock_run.mock_calls))
        with patch.object(Flask, 'wsgi_app', autospec=True) as (mock_run):
            wsgi([], None)
        self.assertEqual(1, len(mock_run.mock_calls))
        return

    def test_run_debug(self):
        with patch.object(Flask, 'run', autospec=True) as (mock_run):
            debug()
        self.assertEqual(1, len(mock_run.mock_calls))

    def test_app_factory(self):
        ret = app_factory(None)
        self.assertEqual(ret, wsgi)
        return