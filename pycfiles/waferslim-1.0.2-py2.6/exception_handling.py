# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/waferslim/examples/exception_handling.py
# Compiled at: 2010-02-27 16:51:07
"""
Example of throwing exceptions from fixtures
See http://localhost:8080/FitNesse.UserGuide.SliM.ExceptionHandling

Fitnesse table markup:

|import|
|waferslim.examples.exception_handling|

|script|exceptional|
|raise exception|whoops|
|stop test|no more!|
|should not be called|

|script|should not be called|

"""
from waferslim import StopTestException

class Exceptional:
    """ Class to illustrate exception handling """

    def raise_exception(self, message):
        """ Raise an exception with message """
        raise Exception(message)

    def stop_test(self, message):
        """ Halt further test execution with message """
        raise StopTestException(message)