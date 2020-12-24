# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_expose.py
# Compiled at: 2016-04-02 06:58:01
from __future__ import unicode_literals
from __future__ import print_function
import unittest, os
from moya import db
from moya import pilot
from moya.wsgi import WSGIApplication
from moya.console import Console
from moya.context import Context
from moya.context.tools import set_dynamic

class TestExpose(unittest.TestCase):
    """Test exposed Python code in a project."""

    def setUp(self):
        _path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(_path, b'testproject')
        self.application = WSGIApplication(path, b'settings.ini', strict=True, validate_db=False, disable_autoreload=True)
        console = Console()
        self.archive = self.application.archive
        db.sync_all(self.archive, console)
        self.context = context = Context()
        self.archive.populate_context(context)
        self.application.populate_context(context)
        set_dynamic(context)
        context[b'.console'] = console

    def tearDown(self):
        del self.archive
        del self.application

    def test_macros(self):
        app = self.archive.apps[b'site']
        self.assertEqual(6, self.archive(b'macro.expose.double', self.context, app, n=3))
        self.assertEqual(21, self.archive(b'macro.expose.tripple', self.context, app, n=7))

    def test_filters(self):
        app = self.archive.apps[b'site']
        self.context[b'.app'] = app
        with pilot.manage(self.context):
            self.assertEqual(1000, self.context.eval(b"10|'cube'"))
            self.assertEqual(1000, self.context.eval(b"10|'cube from site'"))
            self.assertEqual(1000, self.context.eval(b'10|.app.filters.cube'))