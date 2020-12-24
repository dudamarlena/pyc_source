# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_calls.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
import unittest, os
from fs.opener import open_fs
from moya.context import Context
from moya.console import Console
from moya.archive import Archive

class TestCalls(unittest.TestCase):

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

    def test_moya_call_no_lazy(self):
        """Test moya call without lazy attribute"""
        self.archive(b'moya.tests#test_moya_call_no_lazy', self.context, None)
        self.assert_(self.context.root[b'called'])
        self.assertEqual(self.context[b'.result'], 123)
        return

    def test_moya_call_lazy(self):
        """Test lazy moya calls"""
        self.archive(b'moya.tests#test_moya_call_lazy', self.context, None)
        self.assert_(b'called' not in self.context.root)
        self.assertEqual(self.context[b'result'], 123)
        self.assert_(b'called' in self.context.root)
        self.assert_(self.context.root[b'called'])
        return