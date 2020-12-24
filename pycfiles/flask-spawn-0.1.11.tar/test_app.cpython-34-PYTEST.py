# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattpease/DevTools/Workspaces/flask-spawn/flaskspawn/cookiecutters/small/{{cookiecutter.repo_name}}/tests/test_app.py
# Compiled at: 2015-07-14 18:38:14
# Size of source mod 2**32: 313 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from application.views import app
import unittest, os

class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config.from_object(os.environ.get('SETTINGS'))
        self.app = app.test_client()

    def test_health(self):
        self.assertEqual(self.app.get('/health').status, '200 OK')