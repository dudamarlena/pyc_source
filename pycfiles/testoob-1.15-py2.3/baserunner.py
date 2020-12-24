# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/baserunner.py
# Compiled at: 2009-10-07 18:08:46
"""Useful base class for runners"""
import testoob.asserter

class BaseRunner(object):
    """default implementations of setting a reporter and done()"""
    __module__ = __name__

    def __init__(self):
        self.reporter = None
        return

    def run(self, fixture):
        testoob.asserter.Asserter().set_reporter(fixture.get_fixture(), self.reporter)

    def done(self):
        self.reporter.done()

    def isSuccessful(self):
        return self.reporter.isSuccessful()