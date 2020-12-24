# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/DemoPackage/tests/test_utils.py
# Compiled at: 2013-04-29 13:17:22
""" File to test the utility functions."""
import unittest, DemoPackage.utils

class TestUtils(unittest.TestCase):
    """Unittest Class
    """

    def setUp(self):
        """ Unittest setup function and declares a Sequence of 10 numbers.
        
        :param self: 
        :returns: None
        """
        self.seq = range(10)

    def test_print_integer(self):
        """Testing the print_integer function.
        
        :param self:
        :returns: None
        """
        print 'Sequence : ', self.seq
        DemoPackage.utils.print_integer()

    def test_print_string(self):
        """Testing the print_string function.
        
        :param self:
        :returns: None
        """
        print 'Sequence : ', self.seq
        DemoPackage.utils.print_string()


if __name__ == '__main__':
    unittest.main()