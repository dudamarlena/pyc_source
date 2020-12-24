# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_content.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
import unittest, os
from fs.opener import open_fs
from moya.context import Context
from moya.console import Console
from moya.archive import Archive
from moya.content import Content

class TestContent(unittest.TestCase):

    def setUp(self):
        self.called = False
        path = os.path.abspath(os.path.dirname(__file__))
        self.fs = open_fs(path)
        self.context = Context()
        self.context[b'console'] = Console()
        self.archive = Archive()
        import_fs = self.fs.opendir(b'archivetest')
        self.archive.load_library(import_fs)
        self.archive.finalize()

    def test_content(self):
        value = self.archive(b'moya.tests#test_render_content', self.context, None)
        self.assertEqual(value, b'<strong>bold</strong>')
        self.archive(b'moya.tests#test_render_content_2', self.context, None)
        self.assertEqual(self.context[b'.html'], b'<em>emphasize</em>')
        return