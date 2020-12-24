# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/tests/test_core.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from reviewboard.scmtools.core import ChangeSet, Commit
from reviewboard.testing.testcase import TestCase

class CoreTests(TestCase):
    """Tests for the scmtools.core module"""

    def test_empty_changeset(self):
        """Testing ChangeSet defaults"""
        cs = ChangeSet()
        self.assertEqual(cs.changenum, None)
        self.assertEqual(cs.summary, b'')
        self.assertEqual(cs.description, b'')
        self.assertEqual(cs.branch, b'')
        self.assertTrue(len(cs.bugs_closed) == 0)
        self.assertTrue(len(cs.files) == 0)
        return


class CommitTests(TestCase):
    """Tests for reviewboard.scmtools.core.Commit"""

    def test_diff_byte_string(self):
        """Testing Commit initialization with diff as byte string"""
        commit = Commit(diff=b'hi … there')
        self.assertIsInstance(commit.diff, bytes)
        self.assertEqual(commit.diff, b'hi … there')

    def test_diff_unicode_string(self):
        """Testing Commit initialization with diff as unicode string"""
        commit = Commit(diff=b'hi … there')
        self.assertIsInstance(commit.diff, bytes)
        self.assertEqual(commit.diff, b'hi … there')