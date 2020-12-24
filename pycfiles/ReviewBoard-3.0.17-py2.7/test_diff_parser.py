# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_diff_parser.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from reviewboard.diffviewer.parser import DiffParser
from reviewboard.testing import TestCase

class DiffParserTest(TestCase):
    """Unit tests for DiffParser."""

    def test_form_feed(self):
        """Testing DiffParser with a form feed in the file"""
        data = b'--- README  123\n+++ README  (new)\n@@ -1,4 +1,6 @@\n Line 1\n Line 2\n+\x0c\n+Inserted line\n Line 3\n Line 4\n'
        files = DiffParser(data).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].insert_count, 2)
        self.assertEqual(files[0].delete_count, 0)
        self.assertEqual(files[0].data, data)

    def test_line_counts(self):
        """Testing DiffParser with insert/delete line counts"""
        diff = b'+ This is some line before the change\n- And another line\nIndex: foo\n- One last.\n--- README  123\n+++ README  (new)\n@@ -1,1 +1,1 @@\n-blah blah\n-blah\n+blah!\n-blah...\n+blah?\n-blah!\n+blah?!\n'
        files = DiffParser(diff).parse()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].insert_count, 3)
        self.assertEqual(files[0].delete_count, 4)