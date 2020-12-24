# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/infomedia/dist/run_unit_tests.py
# Compiled at: 2012-07-20 17:10:40
import os, sys, types, unittest
from unittest import *

class TestProgram:
    """A command-line program that runs a set of tests; this is primarily
       for making test modules conveniently executable.
    """
    USAGE = "Usage: %(progName)s [options] [test] [...]\n\nOptions:\n  -h, --help       Show this message\n  -v, --verbose    Verbose output\n  -q, --quiet      Minimal output\n\nExamples:\n  %(progName)s                               - run default set of tests\n  %(progName)s MyTestSuite                   - run suite 'MyTestSuite'\n  %(progName)s MyTestCase.testSomething      - run MyTestCase.testSomething\n  %(progName)s MyTestCase                    - run all 'test*' test methods\n                                               in MyTestCase\n"

    def __init__(self, module='__main__', defaultTest=None, argv=None, testRunner=None, testLoader=defaultTestLoader):
        if type(module) == type(''):
            self.module = __import__(module)
            for part in module.split('.')[1:]:
                self.module = getattr(self.module, part)

        else:
            self.module = module
        if argv is None:
            argv = sys.argv
        self.verbosity = 1
        self.defaultTest = defaultTest
        self.testRunner = testRunner
        self.testLoader = testLoader
        self.progName = os.path.basename(argv[0])
        self.parseArgs(argv)
        self.runTests()
        return

    def usageExit(self, msg=None):
        if msg:
            print msg
        print self.USAGE % self.__dict__
        sys.exit(2)

    def parseArgs(self, argv):
        import getopt
        try:
            options, args = getopt.getopt(argv[1:], 'hHvq', [
             'help', 'verbose', 'quiet'])
            for opt, value in options:
                if opt in ('-h', '-H', '--help'):
                    self.usageExit()
                if opt in ('-q', '--quiet'):
                    self.verbosity = 0
                if opt in ('-v', '--verbose'):
                    self.verbosity = 2

            if len(args) == 0 and self.defaultTest is None:
                self.test = self.testLoader.loadTestsFromModule(self.module)
                return
            if len(args) > 0:
                self.testNames = args
            else:
                self.testNames = (
                 self.defaultTest,)
            self.createTests()
        except getopt.error as msg:
            self.usageExit(msg)

        return

    def createTests(self):
        print self.testNames
        self.test = self.testLoader.loadTestsFromNames(self.testNames)

    def runTests(self):
        if self.testRunner is None:
            self.testRunner = TextTestRunner
        if isinstance(self.testRunner, (type, types.ClassType)):
            try:
                testRunner = self.testRunner(verbosity=self.verbosity)
            except TypeError:
                testRunner = self.testRunner()

        else:
            testRunner = self.testRunner
        result = testRunner.run(self.test)
        sys.exit(not result.wasSuccessful())
        return


main = TestProgram
if __name__ == '__main__':
    main(module=None)