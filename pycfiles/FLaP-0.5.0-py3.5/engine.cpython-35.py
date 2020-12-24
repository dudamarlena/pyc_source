# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\engine.py
# Compiled at: 2016-09-30 02:42:03
# Size of source mod 2**32: 1865 bytes
from unittest import TestCase, main
from flap.engine import Fragment
from flap.util.oofs import File, MissingFile
from flap.util.path import ROOT

class FragmentTest(TestCase):

    def setUp(self):
        self.file = File(None, ROOT / 'main.tex', 'xxx')
        self.fragment = Fragment(self.file, 13, 'blah blah')

    def test_expose_line_number(self):
        self.assertEqual(self.fragment.line_number(), 13)

    def test_reject_negative_or_zero_line_number(self):
        with self.assertRaises(ValueError):
            Fragment(self.file, 0, 'blah blah')

    def test_expose_file(self):
        self.assertEqual(self.fragment.file().fullname(), 'main.tex')

    def test_reject_missing_file(self):
        with self.assertRaises(ValueError):
            Fragment(MissingFile(ROOT / 'main.tex'), 13, 'blah blah')

    def test_expose_fragment_text(self):
        self.assertEqual(self.fragment.text(), 'blah blah')

    def test_detect_comments(self):
        self.assertFalse(self.fragment.is_commented_out())

    def test_should_be_sliceable(self):
        self.assertEqual(self.fragment[0:4].text(), 'blah')


if __name__ == '__main__':
    main()