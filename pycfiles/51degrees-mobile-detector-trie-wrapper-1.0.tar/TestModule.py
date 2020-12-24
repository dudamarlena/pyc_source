# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\TestSuite\TestModule.py
# Compiled at: 2006-08-11 10:50:12
__doc__ = '\nProvides the TestModule class for wrapping modules/packages.\n\nCopyright 2006 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import os
from Ft.Lib import ImportUtil
import TestLoader, TestFunction, TestMode, TestCoverage

class TestModule(TestLoader.TestLoader):
    """Test object for a module or package."""
    __module__ = __name__

    def __init__(self, name, module, addModes, skipModes, allModes):
        TestLoader.TestLoader.__init__(self, name, module.__name__, addModes, skipModes, allModes)
        self.module = module
        self.modes = self.getModes(addModes, skipModes, allModes)
        loader = ImportUtil.FindLoader(self.path)
        self.isPackage = loader.is_package(self.path)
        return

    def getModes(self, addModes, skipModes, allModes):
        modes = getattr(self.module, 'MODES', [TestMode.DefaultMode()])
        run_modes = []
        if allModes:
            for mode in modes:
                if mode.name not in skipModes:
                    run_modes.append(mode)

        else:
            for mode in modes:
                if mode.name in addModes and mode.name not in skipModes:
                    run_modes.append(mode)

            if not run_modes:
                for mode in modes:
                    if mode.default and mode.name not in skipModes:
                        run_modes.append(mode)

        return run_modes

    def getTests(self):
        """
        Get the test objects contained within this module.
        """
        if not self.tests:
            for name in dir(self.module):
                if name == 'Test':
                    obj = getattr(self.module, name)
                    if callable(obj):
                        self.tests.append(TestFunction.TestFunction(obj))

            if self.isPackage:
                files = []
                dirs = []
                path = ImportUtil.GetSearchPath(self.path)
                for (importer, name, ispkg) in ImportUtil.IterModules(path):
                    if ispkg:
                        dirs.append(name)
                    else:
                        files.append(name)

                dirs.sort()
                files.sort()
                if hasattr(self.module, 'PreprocessFiles'):
                    (dirs, files) = self.module.PreprocessFiles(dirs, files)
                for name in dirs + files:
                    self.addTest(name)

                if hasattr(self.module, 'CoverageModule'):
                    ignored = None
                    if hasattr(self.module, 'CoverageIgnored'):
                        ignored = self.module.CoverageIgnored
                    ct = TestCoverage.TestCoverage(self.module.CoverageModule, ignored)
                    self.tests.insert(0, TestFunction.TestFunction(ct._start))
                    self.tests.append(TestFunction.TestFunction(ct._end))
        return self.tests
        return

    def showTests(self, indent):
        if self.isPackage:
            print '%s%s%s' % (indent, self.name, os.sep)
            new_indent = indent + ' ' * 2
            for test in self.getTests():
                test.showTests(new_indent)

        else:
            print '%s%s' % (indent, self.name)
        return

    def run(self, tester):
        tester.startGroup(self.name)
        modes = []
        for mode in self.modes:
            if mode.initialize(tester):
                modes.append(mode)

        if not modes:
            tester.warning('All modes have been skipped')
        for mode in modes:
            mode.start(tester)
            try:
                have_run = 0
                for test in self.getTests():
                    self.runTest(tester, test)
                    have_run = 1

                if not have_run:
                    tester.warning('Module does define any tests')
            finally:
                mode.finish(tester)

        tester.groupDone()
        return

    def runTest(self, tester, testObject):
        depth = len(tester.groups)
        try:
            testObject.run(tester)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            tester.exception('Unhandled exception in test')
            if tester.test:
                tester.testDone()
            while len(tester.groups) > depth:
                tester.groupDone()

            return

        if tester.test:
            tester.warning('Failed to finish test (fixed)')
            tester.testDone()
        count = len(tester.groups) - depth
        if count < 0:
            tester.error('Closed too many groups')
        elif count > 0:
            tester.warning('Failed to close %d groups (fixed)' % count)
            while count:
                count -= 1
                tester.message('Closing group %s' % tester.groups[(-1)])
                tester.groupDone()

        return