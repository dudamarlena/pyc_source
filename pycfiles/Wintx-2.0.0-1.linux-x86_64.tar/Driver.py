# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/drivers/dummy/Driver.py
# Compiled at: 2016-03-23 14:50:19
"""Dummy driver for unittesting."""

class Driver(object):

    def __init__(self, test_required=None, test_required_int=None):
        self.value = 'success'
        self.abort_value = 'abort'
        self.test_required = test_required
        self.test_required_int = test_required_int

    def testFunction(self):
        return True

    def testValue(self, value):
        return value