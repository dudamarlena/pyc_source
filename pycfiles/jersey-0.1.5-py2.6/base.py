# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jersey/cases/base.py
# Compiled at: 2010-11-11 16:08:49
import os
from twisted.python import log, reflect
from twisted.enterprise.adbapi import ConnectionPool
from zope.interface.exceptions import DoesNotImplement
from zope.interface.verify import verifyObject

class TestBase(object):
    """Base class for tests.  Does not subclass TestCase.
    """

    def makeTestRoot(self):
        """Create a test-specific directory."""
        pathParts = self.id().split('.')
        try:
            casesIdx = pathParts.index('cases')
        except IndexError:
            self.rootDir = os.path.sep.join(pathParts)
        else:
            self.rootDir = os.path.sep.join(pathParts[casesIdx + 1:])

        os.makedirs(self.rootDir)
        return self.rootDir

    def assertImplements(self, interface, obj):
        """Fail if obj does not implement interface."""
        try:
            verifyObject(interface, obj)
        except DoesNotImplement, dni:
            self.fail(('{0!r}: {1!s}').format(obj, dni))

    failIfNotImplements = assertImplements