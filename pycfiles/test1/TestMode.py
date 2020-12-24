# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\TestSuite\TestMode.py
# Compiled at: 2002-07-18 13:15:58
"""
Provides the TestMode base class for testing modes.

Copyright 2002 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
__revision__ = '$Id: TestMode.py,v 1.2 2002-07-18 18:15:58 molson Exp $'

class TestMode:
    __module__ = __name__

    def __init__(self, name, default):
        self.name = name
        self.default = default
        self.initialized = None
        return
        return

    def initialize(self, tester):
        """
        Called the first time this mode is used. A return value of false
        signals that this mode is not to be used.
        """
        if self.initialized is None:
            self.initialized = self._init(tester)
        return self.initialized
        return

    def start(self, tester):
        """
        Called before beginning any tests.
        """
        tester.startGroup(self.name)
        self._pre(tester)
        return

    def finish(self, tester):
        """
        Called when all tests have run to completion (or exception).
        """
        self._post(tester)
        tester.groupDone()
        return

    def _init(self, tester):
        return 1

    def _pre(self, tester):
        pass

    def _post(self, tester):
        pass


class DefaultMode(TestMode):
    __module__ = __name__

    def __init__(self):
        TestMode.__init__(self, '', 1)
        return

    def initialize(self, tester):
        return 1

    def start(self, tester):
        return

    def finish(self, tester):
        return