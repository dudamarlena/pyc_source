# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/common/test_tools.py
# Compiled at: 2015-06-14 13:30:57
from __future__ import absolute_import
import os
from seedbox.common import tools
from seedbox.tests import test

class ToolsTest(test.BaseTestCase):

    def test_verify_path(self):
        self.assertIsNotNone(tools.verify_path(os.getcwd()))
        self.assertIsNotNone(tools.verify_path(os.path.expanduser('~')))
        self.assertIsNotNone(tools.verify_path('.'))
        self.assertIsNotNone(tools.verify_path('/lib'))
        self.assertIsNone(tools.verify_path('library'))
        self.assertIsNone(tools.verify_path('missing'))
        self.assertIsNone(tools.verify_path('/to/be/found/'))
        self.assertIsNone(tools.verify_path(os.path.join(os.getcwd(), 'junk-tmp-simple-duh.txt')))

    def test_format_file_ext(self):
        self.assertIsInstance(tools.format_file_ext([]), list)
        self.assertEqual(len(tools.format_file_ext([])), 0)
        self.assertIsInstance(tools.format_file_ext(''), list)
        self.assertEqual(len(tools.format_file_ext('')), 0)
        self.assertIsInstance(tools.format_file_ext([' ']), list)
        self.assertEqual(len(tools.format_file_ext([' '])), 0)
        self.assertIsInstance(tools.format_file_ext(None), list)
        self.assertEqual(len(tools.format_file_ext(None)), 0)
        self.assertEqual(len(tools.format_file_ext(['.avi', None, '.mp4', None, ''])), 2)
        self.assertEqual(len(tools.format_file_ext(['.avi', '.mp4'])), 2)
        self.assertEqual(len(tools.format_file_ext(['avi', 'mp4'])), 2)
        self.assertEqual(len(tools.format_file_ext(['avi', '.mp4'])), 2)
        self.assertEqual(len(tools.format_file_ext(['.avi', 'mp4'])), 2)
        for ext in ['.avi', '.mp4', 'avi', 'mp4']:
            ext_list = tools.format_file_ext([ext])
            self.assertEqual(len(ext_list[0]), 4)

        return