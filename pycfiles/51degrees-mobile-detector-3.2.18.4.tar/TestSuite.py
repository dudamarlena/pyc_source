# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\TestSuite\TestSuite.py
# Compiled at: 2006-08-11 10:50:12
__doc__ = '\nProvides the TestSuite class, which represents the package(s) to test.\n\nCopyright 2006 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
__revision__ = '$Id: TestSuite.py,v 1.13 2006-08-11 15:50:12 jkloth Exp $'
import getopt, sys, os, inspect
from types import *
import TestLoader, TestModule, Tester
from Errors import *
USAGE = "Usage:\n  %(script)s [options] [test] [...]\n  %(script)s --help-tests\n  %(script)s --help\n  %(script)s --help [test]\n\nExamples:\n  %(script)s                        run default set of tests\n  %(script)s directory              run all tests in 'directory'\n  %(script)s directory%(sep)sfile         run just 'file' from 'directory'\n"

class TestSuite:
    """
    A command-line program that runs a set of tests; this is primarily
    for making test modules conveniently executable.
    """
    __module__ = __name__
    options = [
     (
      'help', 'h', 'Show detailed help message'), ('help-tests', 't', 'List all available tests'), ('verbose', 'v', 'Increase display verbosity'), ('quiet', 'q', 'Decrease display verbosity'), ('mode=', 'm', 'Add mode to default modes to run'), ('skip=', 'k', 'Remove a mode from the modes to run'), ('full', 'f', 'Use all modes'), ('stop', 's', 'Stop on errors'), ('nocolor', 'n', 'Disable ANSI color sequences'), ('noreport', 'r', 'Disable report generation'), ('outfile=', 'o', 'Specify an output file for all results'), ('offline', 'l', 'Skip tests requiring internet connection')]
    negative_opts = {'quiet': 'verbose', 'nocolor': 'color', 'noreport': 'report'}
    boolean_opts = (
     'full', 'stop', 'nocolor', 'noreport', 'offline', 'help', 'help-tests')

    def __init__(self, attrs):
        self.verbose = 2
        self.mode = []
        self.skip = []
        self.full = 0
        self.stop = 0
        self.color = 1
        self.report = 1
        self.outfile = ''
        self.offline = 0
        self.help = 0
        self.help_tests = 0
        self.script_name = None
        self.script_args = None
        self.name = None
        self.packages = None
        for (key, value) in attrs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise TestSuiteSetupError('invalid test option %r' % key)

        return
        return

    def _grokOptions(self):
        long_opts = []
        short_opts = []
        short2long = {}
        for option in self.options:
            try:
                (long, short, help) = option
            except ValueError:
                raise TestSuiteInternalError, 'invalid option tuple %r' % option

            if not isinstance(long, StringType) or len(long) < 2:
                raise TestSuiteInternalError, 'invalid long option %r' % long
            if short and not isinstance(short, StringType) and len(short) > 1:
                raise TestSuiteInternalError, 'invalid short option %r' % short
            long_opts.append(long)
            if short:
                if long.endswith('='):
                    short = short + ':'
                    long = long[:-1]
                short2long[short[0]] = long
                short_opts.append(short)

        return (('').join(short_opts), long_opts, short2long)

    def _getopt(self, args):
        (short_opts, long_opts, short2long) = self._grokOptions()
        parsed_args = []
        parsed_opts = []
        while args:
            try:
                (opts, args) = getopt.getopt(args, short_opts, long_opts)
            except getopt.error, error:
                raise TestSuiteArgumentError(str(error))

            for (opt, value) in opts:
                if len(opt) == 2 and opt[0] == '-':
                    opt = short2long[opt[1]]
                else:
                    opt = opt[2:]
                parsed_opts.append((opt, value))

            while args and args[0][:1] != '-':
                arg = args.pop(0)
                pathname = os.path.normpath(arg)
                if os.path.isdir(pathname):
                    source = pathname + os.sep + '__init__.py'
                    compiled = source + (__debug__ and 'c' or 'o')
                    if os.path.exists(source) or os.path.exists(compiled):
                        arg = pathname.replace(os.sep, '.')
                elif os.path.exists(pathname):
                    modulename = inspect.getmodulename(pathname)
                    if modulename is not None:
                        names = pathname.split(os.sep)
                        names[-1] = modulename
                        arg = ('.').join(names)
                parsed_args.append(arg)

        for (name, value) in parsed_opts:
            if name in self.boolean_opts:
                value = 1
            alias = self.negative_opts.get(name)
            if alias:
                attr = alias.replace('-', '_')
            else:
                attr = name.replace('-', '_')
            if not hasattr(self, attr):
                raise TestSuiteInternalError, 'missing attribute for option %r' % name
            current = getattr(self, attr)
            if name in self.boolean_opts:
                if alias:
                    setattr(self, attr, 0)
                else:
                    setattr(self, attr, 1)
            elif isinstance(current, IntType):
                if alias:
                    setattr(self, attr, current - 1)
                else:
                    setattr(self, attr, current + 1)
            elif isinstance(current, ListType):
                if alias:
                    while value in current:
                        current.remove(value)

                else:
                    current.append(value)
            elif isinstance(current, StringType):
                setattr(self, attr, value)
            else:
                raise TestSuiteInternalError, 'unknown type for option %r' % name

        return parsed_args
        return

    def addTests(self, packages):
        for package in packages:
            testobj = self.test
            for step in package.split('.'):
                for test in testobj.tests:
                    if test.name == step:
                        testobj = test
                        break
                else:
                    testobj = testobj.addTest(step)

        return

    def parseCommandLine(self):
        """
        Parse the test script's command line, taken from the 'script_args'
        instance attribute (which defaults to 'sys.argv[1:]').  This is
        first processed for options that set attributes of the TestSuite
        instance.  Then, it is scanned for test arguments.
        """
        packages = self._getopt(self.script_args)
        self.test = TestLoader.TestLoader(self.name, '', self.mode, self.skip, self.full)
        if self.help_tests:
            print self.generateUsage()
            print 'Available tests:'
            self.showTests()
            return 0
        if self.help:
            self.showHelp(packages)
            return 0
        self.addTests(packages or self.packages)
        return 1

    def showTests(self):
        indent = ' ' * 2
        self.addTests(self.packages)
        for test in self.test.getTests():
            test.showTests(indent)

        return

    def generateUsage(self):
        usage = USAGE % {'script': os.path.basename(self.script_name), 'sep': os.sep}
        return usage

    def showHelp(self, tests):
        print self.generateUsage()
        print 'Options:'
        display_opts = []
        max_opt = 0
        for opt in self.options:
            long = opt[0]
            if long[(-1)] == '=':
                long = '%s<%s>' % (long, long[:-1])
            display = '-%s, --%s' % (opt[1], long)
            display_opts.append((display, opt[2]))
            if len(display) > max_opt:
                max_opt = len(display)

        for (display, help) in display_opts:
            print '  %-*s  %s' % (max_opt, display, help)

        print
        for path in tests:
            modes = []
            testobj = self.test
            for step in path.split('.'):
                testobj = testobj.loadTest(step)
                for mode in testobj.getModes([], [], 1):
                    if mode.name:
                        modes.append((mode.name, testobj.path))

            if modes:
                print 'Modes for %r:' % testobj.path
                for (name, path) in modes:
                    if path != testobj.path:
                        print '  %s (declared in %s)' % (name, path)
                    else:
                        print '  %s' % name

                print
            subtests = [ test for test in testobj.getTests() if isinstance(test, TestModule.TestModule) ]
            if subtests:
                print 'Sub-tests for %r:' % testobj.path
                for test in subtests:
                    print '  %s' % test.name

                print

        return

    def runTests(self):
        tester = Tester.Tester(self.stop, self.color, self.verbose)
        tester.offline = self.offline
        try:
            for test in self.test.getTests():
                test.run(tester)

        except KeyboardInterrupt:
            sys.stderr.write('\n%s\n' % ('=' * 72))
            sys.stderr.write('\nTesting interrupted\n')

        if self.report:
            tester.report()
        return