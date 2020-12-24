# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/profilemetest.py
# Compiled at: 2015-05-28 05:23:50
from nose import with_setup
import unittest, os
from pycast.common import profileMe

class ProfileMeDecoratorTest(unittest.TestCase):
    """Test class containing all tests for the @profileMe decorator."""

    def setUp(self):
        """Initializes the environment for each test."""
        self.statfiles = [
         'statfile1', 'statfile2']

    def tearDown(self):
        """This function gets called after each test function."""
        for statfile in self.statfiles:
            if os.path.isfile(statfile):
                os.remove(statfile)

    def profile_data_creation_test(self):
        """Testing successfull profile data creation."""
        statfile = self.statfiles[0]

        @profileMe(statfile)
        def dummy_func():
            """This is an (nearly) empty dummy function that nees to be profiled.

            The functions evaluates, if the formula for the gaussian sum is correct.
            """
            sumUpTo = 1000
            summedVals = sum(xrange(sumUpTo + 1))
            easySum = sumUpTo * (sumUpTo + 1) / 2
            return easySum == summedVals

        booleanVal = dummy_func()
        assert booleanVal
        assert os.path.isfile(statfile)

    def profile_function_name_test(self):
        """Test the validity of __name__ for any decorated function."""
        statfile = self.statfiles[0]

        @profileMe(statfile)
        def dummy_func():
            """This is an (nearly) empty dummy function that nees to be profiled.

            The functions evaluates, if the formula for the gaussian sum is correct.
            """
            sumUpTo = 1000
            summedVals = sum(xrange(sumUpTo + 1))
            easySum = sumUpTo * (sumUpTo + 1) / 2
            return easySum == summedVals

        booleanVal = dummy_func()
        assert booleanVal
        assert dummy_func.__name__ == 'dummy_func'

    def profile_doc_string_test(self):
        """Test the validity of __doc__ for any decorated function."""
        statfile = self.statfiles[0]

        @profileMe(statfile)
        def dummy_func():
            """StupidDocString"""
            sumUpTo = 1000
            summedVals = sum(xrange(sumUpTo + 1))
            easySum = sumUpTo * (sumUpTo + 1) / 2
            return easySum == summedVals

        booleanVal = dummy_func()
        assert booleanVal
        assert dummy_func.__doc__ == 'StupidDocString'