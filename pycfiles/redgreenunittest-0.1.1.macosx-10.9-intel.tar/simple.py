# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/redgreenunittest/django/simple.py
# Compiled at: 2013-05-11 00:36:41
from django.test.simple import DjangoTestSuiteRunner
import redgreenunittest

class RedGreenTestSuiteRunner(DjangoTestSuiteRunner):

    def run_suite(self, suite, **kwargs):
        return redgreenunittest.TextTestRunner(verbosity=self.verbosity, failfast=self.failfast).run(suite)