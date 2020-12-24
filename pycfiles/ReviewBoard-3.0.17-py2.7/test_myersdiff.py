# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_myersdiff.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from reviewboard.diffviewer.myersdiff import MyersDiffer
from reviewboard.testing import TestCase

class MyersDifferTest(TestCase):
    """Unit tests for MyersDiffer."""

    def test_equals(self):
        """Testing MyersDiffer with equal chunk"""
        self._test_diff([b'1', b'2', b'3'], [
         b'1', b'2', b'3'], [
         ('equal', 0, 3, 0, 3)])

    def test_delete(self):
        """Testing MyersDiffer with delete chunk"""
        self._test_diff([b'1', b'2', b'3'], [], [
         ('delete', 0, 3, 0, 0)])

    def test_insert_before_lines(self):
        """Testing MyersDiffer with insert before existing lines"""
        self._test_diff(b'1\n2\n3\n', b'0\n1\n2\n3\n', [
         ('insert', 0, 0, 0, 2),
         ('equal', 0, 6, 2, 8)])

    def test_replace_insert_between_lines(self):
        """Testing MyersDiffer with replace and insert between existing lines
        """
        self._test_diff(b'1\n2\n3\n7\n', b'1\n2\n4\n5\n6\n7\n', [
         ('equal', 0, 4, 0, 4),
         ('replace', 4, 5, 4, 5),
         ('insert', 5, 5, 5, 9),
         ('equal', 5, 8, 9, 12)])

    def _test_diff(self, a, b, expected):
        opcodes = list(MyersDiffer(a, b).get_opcodes())
        self.assertEqual(opcodes, expected)