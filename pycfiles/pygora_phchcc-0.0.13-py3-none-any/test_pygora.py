# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/alfredo/python/vpygora/pygora/tests/test_pygora.py
# Compiled at: 2010-09-16 20:46:02
import sys
if '../' not in sys.path:
    sys.path.append('../')
import unittest, os
from pygora import Pygora
import shutil

class TestPygora(unittest.TestCase):

    def setUp(self):
        if os.path.isdir('/tmp/pygora'):
            shutil.rmtree('/tmp/pygora')
        os.mkdir('/tmp/pygora')
        source_file = open('/tmp/pygora/source.py', 'w')
        test_file = open('/tmp/pygora/test_source.py', 'w')
        ignore_file = open('/tmp/pygora/ignoreme.py', 'w')
        ignore_file.write('some source code')
        ignore_file.close()
        source_file.write('# comment line\n        def a_func():\n        "docstring"\n        pass\n        ')
        source_file.close()
        test_file.write('def test_source():\n        pass')
        test_file.close()

    def tearDown(self):
        try:
            os.remove('/tmp/pygora')
        except Exception:
            pass

    def test_test_lines(self):
        """Test lines should always be cero"""
        goat = Pygora(path='.')
        expected = 0
        actual = goat.test_lines
        self.assertEqual(actual, expected)

    def test_source_lines(self):
        """Source lines should always be cero"""
        goat = Pygora(path='.')
        expected = 0
        actual = goat.source_lines
        self.assertEqual(actual, expected)

    def test_path(self):
        """Path should always be the cwd"""
        expected = os.getcwd()
        goat = Pygora()
        actual = goat.path
        self.assertEqual(actual, expected)

    def test_skip_line_comment(self):
        """Return False if line starts with #"""
        goat = Pygora()
        line = '# a commented out line'
        actual = goat.skip_line(line)
        self.assertFalse(actual)

    def test_skip_line_docstring(self):
        """Do NOT Return False if line starts with quote"""
        goat = Pygora()
        line = '"a docstring" '
        actual = goat.skip_line(line)
        self.assertTrue(actual)

    def test_skip_line_empty(self):
        """Return False if line is empty"""
        goat = Pygora()
        line = ' '
        actual = goat.skip_line(line)
        self.assertFalse(actual)

    def test_recognize_Test(self):
        """Return Test if the file is a test file"""
        goat = Pygora(path='/tmp/test_source.py')
        actual = goat.test_lines
        expected = 10
        self.assertEqual(actual, expected)

    def test_line_count(self):
        """Return the total number of lines for a file"""
        goat = Pygora()
        expected = '3'
        actual = goat.line_count('/tmp/pygora/source.py')
        self.assertEqual(actual, expected)

    def test_line_count_test(self):
        """Return the total number of lines for a test files"""
        goat = Pygora()
        expected = '2'
        actual = goat.line_count('/tmp/pygora/test_source.py')
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()