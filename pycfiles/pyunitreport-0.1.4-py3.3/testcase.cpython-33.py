# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/examples/testcase.py
# Compiled at: 2017-11-06 22:30:35
# Size of source mod 2**32: 1002 bytes
from pyunitreport import HTMLTestRunner
import unittest

class TestStringMethods(unittest.TestCase):
    __doc__ = ' Example test for HtmlRunner. '

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)

    def test_error(self):
        """ This test should be marked as error one. """
        raise ValueError

    def test_fail(self):
        """ This test should fail. """
        self.assertEqual(1, 2)

    @unittest.skip('This is a skipped test.')
    def test_skip(self):
        """ This test should be skipped. """
        pass


if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner(output='example_dir'))