# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/ftpysetup/runtest/runner.py
# Compiled at: 2014-12-30 15:36:44
# Size of source mod 2**32: 2706 bytes
"""Setuptools command to execute all tests. This is useful for continuous
integration systems."""
__author__ = ('Lance Finn Helsten', )
__version__ = '0.7.3'
__copyright__ = 'Copyright (C) 2014 Lance Helsten'
__docformat__ = 'reStructuredText en'
__license__ = '\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n'
import sys, setuptools
__all__ = [
 'TestRunner']

class TestRunner(setuptools.Command):
    description = 'Run all unit and acceptance tests on the system.'
    user_options = [
     ('suite=', 's', 'Run specific test suite [default: all tests].'),
     ('level=', 'l', 'Test suite level to run: smoke, sanity, or shakedown.'),
     ('debug=', 'd', 'Debug a specific test with preset breakpoints.'),
     ('coverage', 'c', 'Turn on code coverage for the tests.'),
     ('bSetup', None, 'Add a breakpoint in setUp for debug.'),
     ('bTeardown', None, 'Add a breakpoint in tearDown for debug.')]

    def initialize_options(self):
        self.suite = []
        self.level = 'sanity'
        self.debug = None
        self.coverage = False
        self.bSetup = False
        self.bTeardown = False

    def finalize_options(self):
        if self.suite is None:
            raise ValueError('suite must be set.')

    def run(self):
        self.reinitialize_command('test_unit', suite=self.suite, debug=self.debug, coverage=self.coverage, bSetup=self.bSetup, bTeardown=self.bTeardown)
        self.run_command('test_unit')
        self.reinitialize_command('test_accept', suite=self.suite, level=self.level, debug=self.debug, coverage=self.coverage, bSetup=self.bSetup, bTeardown=self.bTeardown)
        self.run_command('test_accept')