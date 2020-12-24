# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test_extensions/twill.py
# Compiled at: 2008-11-22 07:58:02
from django.test import TestCase
import twill
from twill import commands as tc

class TwillCommon(TestCase):
    """
    A Base class for using with Twill commands. Provides a few helper methods and setup.
    """

    def setUp(self):
        """Run before all tests in this class, sets the output to the console"""
        twill.set_output(StringIO())

    def find(self, regex):
        """
        By default Twill commands throw exceptions rather than failures when 
        an assertion fails. Here we wrap the Twill find command and return
        the expected response along with a helpful message.     
        """
        try:
            tc.go(self.url)
            tc.find(regex)
        except TwillAssertionError:
            self.fail("No match to '%s' on %s" % (regex, self.url))

    def code(self, status):
        """
        By default Twill commands throw exceptions rather than failures when 
        an assertion fails. Here we wrap the Twill code command and return
        the expected response along with a helpful message.     
        """
        try:
            tc.go(self.url)
            tc.code(status)
        except TwillAssertionError:
            self.fail('%s did not return a %s' % (self.url, status))