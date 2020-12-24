# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_project.py
# Compiled at: 2016-01-11 17:03:58
from __future__ import unicode_literals
from __future__ import print_function
import unittest, os
from moya import db
from moya.wsgi import WSGIApplication
from moya.console import Console
from moya.context import Context
from moya.context.tools import set_dynamic

class TestProject(unittest.TestCase):

    def setUp(self):
        _path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(_path, b'testproject')
        self.application = WSGIApplication(path, b'settings.ini', strict=True, validate_db=False, disable_autoreload=True)
        console = Console()
        self.archive = self.application.archive
        db.sync_all(self.archive, console)
        self.context = context = Context()
        self.application.populate_context(context)
        set_dynamic(context)
        context[b'.console'] = console

    def tearDown(self):
        del self.archive
        del self.application

    def test_content(self):
        """Test content in a project"""
        app = self.archive.apps[b'site']
        html = self.archive(b'site#render_content', self.context, app, content=b'#content.tests.base')
        assert b'[TESTS]' in html
        assert b'<title>[TESTS]</title>' in html
        html = self.archive(b'site#render_content', self.context, app, content=b'#content.tests.merge.replace')
        assert b'[MERGE TEST][B][END MERGE TEST]' in html
        html = self.archive(b'site#render_content', self.context, app, content=b'#content.tests.merge.append')
        assert b'[MERGE TEST][A][B][END MERGE TEST]' in html
        html = self.archive(b'site#render_content', self.context, app, content=b'#content.tests.merge.prepend')
        assert b'[MERGE TEST][B][A][END MERGE TEST]' in html
        html = self.archive(b'site#render_content', self.context, app, content=b'#content.tests.node', var=b'FOO')
        assert b'TEMPLATE VAR FOO' in html