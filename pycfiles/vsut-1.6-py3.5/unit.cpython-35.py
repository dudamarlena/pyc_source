# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vsut/unit.py
# Compiled at: 2016-05-12 03:10:14
# Size of source mod 2**32: 2431 bytes
from collections import namedtuple
from enum import Enum
from math import floor, log10
from sys import stdout
from time import clock
from vsut.assertion import AssertResult

class Unit:
    __doc__ = "A unit is a group of tests, that are run at once.\n\n    Every method of this class, that starts with 'test' will be run automatically,\n    when the run()-method is called.\n    Before and after every test the setup and teardown methods will be called respectively.\n    For every test it's execution time, status, and if necessary an error message are recorded.\n\n        Attributes:\n            tests ({int: str}): A map that maps function names to an unique id.\n            times ({int: str}): A map that maps a functions execution time as a string to its id.\n            results ({int: AssertResult}): A map that maps a tests result to its id. If a test is successful its entry is None.\n    "

    def __init__(self):
        self.tests = {id:funcName for id, funcName in enumerate([method for method in dir(self) if callable(getattr(self, method)) and method.startswith('test')])}
        self.times = {}
        self.results = {}
        self.failed = False
        self.ignoreUnit = False

    def run(self):
        """Runs all tests in this unit.

            Times the execution of all tests and records them.
        """
        for id, name in self.tests.items():
            start = clock()
            try:
                func = getattr(self, name, None)
                self.setup()
                func()
                self.teardown()
            except AssertResult as e:
                result = e
                self.failed = True
            else:
                result = None
            self.results[id] = result
            elapsed = clock() - start
            self.times[id] = '{0:.6f}'.format(elapsed)

    def setup(self):
        """Setup is executed before every test.
        """
        pass

    def teardown(self):
        """Teardown is executed after every test.
        """
        pass