# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/nosexunit/plugin.py
# Compiled at: 2009-09-22 16:55:25
import os, sys, time, logging, StringIO, traceback, nose, nose.util
from nose.plugins import Plugin
import nosexunit.core as ncore, nosexunit.audit as naudit, nosexunit.cover as ncover, nosexunit.const as nconst, nosexunit.tools as ntools, nosexunit.excepts as nexcepts
logger = logging.getLogger('%s.%s' % (nconst.LOGGER, __name__))

class NoseXUnit(Plugin, object):

    def help(self):
        """Help"""
        return 'Output XML report of test status'

    def options(self, parser, env=os.environ):
        """Add launch options for NoseXUnit"""
        Plugin.options(self, parser, env)
        parser.add_option('--core-target', action='store', default=nconst.TARGET_CORE, dest='core_target', help='Output folder for test reports (default is %s).' % nconst.TARGET_CORE)
        parser.add_option('--source-folder', action='store', default=None, dest='source', help='Set source folder (optional for core functionality, required for audit and coverage). Add folder in sys.path.')
        parser.add_option('--search-source', action='store_true', default=False, dest='search_source', help="Walk in the source folder to add deeper folders in sys.path if they don't contain __init__.py file. Works only if --source-folder is defined.")
        parser.add_option('--search-test', action='store_true', default=False, dest='search_test', help='Search tests in folders with no __init__.py file (default: do nothing).')
        parser.add_option('--extra-include', action='append', default=[], dest='extra_include', help='Include packages for audit or coverage processing (default: take all packages in --source-folder, except those defined in --extra-exclude).')
        parser.add_option('--extra-exclude', action='append', default=nconst.AUDIT_COVER_EXCLUDE, dest='extra_exclude', help='Exclude packages for audit or coverage processing (default: %s). Useless if --extra-include defined.' % ((', ').join(nconst.AUDIT_COVER_EXCLUDE),))
        parser.add_option('--extra-test-process', action='store_true', default=False, dest='extra_test_process', help='Include packages matching the test pattern in audit or coverage processing (default: no).')
        parser.add_option('--enable-audit', action='store_true', default=False, dest='audit', help='Use PyLint to audit source code (default: no)')
        parser.add_option('--audit-target', action='store', default=nconst.TARGET_AUDIT, dest='audit_target', help='Output folder for PyLint reports (default is %s).' % nconst.TARGET_AUDIT)
        parser.add_option('--audit-output', action='store', default=nconst.AUDIT_DEFAULT_REPORTER, dest='audit_output', help='Output for audit reports: %s (default: %s).' % ((', ').join(naudit.outputs()), nconst.AUDIT_DEFAULT_REPORTER))
        parser.add_option('--audit-config', action='store', default=None, dest='audit_config', help='Configuration file for PyLint (optional).')
        parser.add_option('--enable-cover', action='store_true', default=False, dest='cover', help='Use coverage to audit source code (default: no)')
        parser.add_option('--cover-target', action='store', default=nconst.TARGET_COVER, dest='cover_target', help='Output folder for coverage reports (default is %s).' % nconst.TARGET_COVER)
        parser.add_option('--cover-clean', action='store_true', default=False, dest='cover_clean', help='Clean previous coverage results (default: no).')
        parser.add_option('--cover-collect', action='store_true', default=False, dest='cover_collect', help='Collect other coverage files potentially generated in cover target folder. These extra files should have the following pattern: %s.* (default: no).' % nconst.COVER_OUTPUT_BASE)
        return

    def configure(self, options, config):
        """Configure the plug in"""
        Plugin.configure(self, options, config)
        self.config = config
        try:
            self.fork = 1 != max(int(options.multiprocess_workers), 1)
        except:
            self.fork = False

        self.core_target = os.path.abspath(options.core_target)
        if options.source:
            self.source = os.path.abspath(options.source)
        else:
            self.source = None
        self.search_source = options.search_source
        self.search_test = options.search_test
        self.extra_include = options.extra_include
        self.extra_exclude = options.extra_exclude
        self.extra_test_process = options.extra_test_process
        self.audit = options.audit
        if self.audit:
            (available, error) = naudit.available()
            if not available:
                raise nexcepts.PluginError('audit not available in NoseXUnit, error while loading dependences: %s' % error)
            self.audit_target = os.path.abspath(options.audit_target)
            if options.audit_config:
                self.audit_config = os.path.abspath(options.audit_config)
            else:
                self.audit_config = None
            self.audit_output = options.audit_output.lower()
        self.cover = options.cover
        if self.cover:
            (available, error) = ncover.available()
            if not available:
                raise nexcepts.PluginError('coverage not available in NoseXUnit, error while loading dependences: %s' % error)
            if self.fork:
                raise nexcepts.PluginError('coverage not available with --processes option')
            self.cover_clean = options.cover_clean
            self.cover_collect = options.cover_collect
            self.cover_target = os.path.abspath(options.cover_target)
        return

    def initialize(self):
        """Set the environment"""
        if self.source and not os.path.isdir(self.source):
            raise nexcepts.NoseXUnitError("source folder doesn't exist: %s" % self.source)
        ntools.create(self.core_target)
        ntools.clean(self.core_target, nconst.PREFIX_CORE, nconst.EXT_CORE)
        self.packages = {}
        if self.source:
            self.packages = ntools.packages(self.source, search=self.search_source)
            folders = []
            for package in self.packages.keys():
                if package.find('.') == -1:
                    folder = os.path.dirname(self.packages[package])
                    if folder not in folders:
                        folders.append(folder)

            backup = sys.path
            sys.path = []
            for folder in folders:
                logger.info('add folder in sys.path: %s' % folder)
                sys.path.append(folder)

            sys.path.extend(backup)
        if self.audit:
            if not self.source:
                raise nexcepts.NoseXUnitError('source folder required for audit')
            if self.audit_output not in naudit.outputs():
                raise nexcepts.NoseXUnitError('output not available for audit: %s' % self.audit_output)
            ntools.create(self.audit_target)
            self.audit_packages = [ package for package in self.packages.keys() if package.find('.') == -1 if self.enable(package) ]
            if self.audit_packages == []:
                raise nexcepts.NoseXUnitError('no package to audit')
            self.audit_cls = naudit.audit(self.source, self.audit_packages, self.audit_output, self.audit_target, self.audit_config)
        else:
            self.audit_cls = []
        if self.cover:
            if not self.source:
                raise nexcepts.NoseXUnitError('source folder required for coverage')
            ntools.create(self.cover_target)
            self.skipped = sys.modules.keys()[:]
            self.cover_packages = [ package for package in self.packages.keys() if self.enable(package) ]
            if self.cover_packages == []:
                raise nexcepts.NoseXUnitError('no package to cover')
            ncover.start(self.cover_clean, self.cover_packages, self.cover_target)

    def enable(self, package):
        """Check if a package has to be processed"""
        if self.conf.testMatch.search(package) and not self.extra_test_process:
            return False
        else:
            if self.extra_include != []:
                return package in self.extra_include
            return package not in self.extra_exclude

    def prepareTest(self, test):
        """Add the generated tests"""
        for audit_test in self.audit_tests:
            test.addTest(audit_test)

    def prepareTestLoader(self, loader):
        """Load the generated tests"""
        self.audit_tests = [ loader.loadTestsFromTestCase(cls) for cls in self.audit_cls ]

    def begin(self):
        """Initialize the plug in"""
        self.initialize()
        self.module = None
        self.suite = None
        self.start = None
        self.stdout = ncore.StdOutRecoder()
        self.stderr = ncore.StdErrRecorder()
        return

    def wantDirectory(self, dirname):
        """Check if search tests in this folder"""
        if self.search_test and not os.path.exists(os.path.join(dirname, nconst.INIT)):
            return True
        else:
            return

    def enableSuite(self, test):
        """Check that suite exists. If not exists, create a new one"""
        current = ntools.get_test_id(test).split('.')[0]
        if self.module != current:
            self.module = current
            self.stopSuite()
            self.startSuite(self.module)

    def startSuite(self, module):
        """Start a new suite"""
        self.suite = ncore.XSuite(module)
        self.suite.start()
        self.stderr.reset()
        self.stdout.reset()
        self.stderr.start()
        self.stdout.start()

    def startTest(self, test):
        """Record starting time"""
        self.enableSuite(test)
        self.start = time.time()

    def addTestCase(self, kind, test, err=None):
        """Add a new test result in the current suite"""
        elmt = ncore.XTest(kind, test, err=err)
        elmt.setStart(self.start)
        elmt.stop()
        self.enableSuite(test)
        self.suite.addTest(elmt)

    def addError(self, test, err):
        """Add a error test"""
        kind = nconst.TEST_ERROR
        if isinstance(test, nose.SkipTest):
            kind = nconst.TEST_SKIP
        elif isinstance(test, nose.DeprecatedTest):
            kind = nconst.TEST_DEPRECATED
        self.addTestCase(kind, test, err=err)

    def addFailure(self, test, err):
        """Add a failure test"""
        self.addTestCase(nconst.TEST_FAIL, test, err=err)

    def addSuccess(self, test):
        """Add a successful test"""
        self.addTestCase(nconst.TEST_SUCCESS, test)

    def stopSuite(self):
        """Stop the current suite"""
        if self.suite != None:
            self.stdout.stop()
            self.stderr.stop()
            self.suite.stop()
            self.suite.setStdout(self.stdout.content())
            self.suite.setStderr(self.stderr.content())
            self.suite.writeXml(self.core_target)
            self.suite = None
        return

    def report(self, stream):
        """Create the report"""
        if self.cover:
            entries = [ package for (entry, package) in sys.modules.items() if self.consider(entry, package) ]
            ncover.stop(stream, entries, self.cover_target, self.cover_collect)

    def consider(self, entry, package):
        """Check if the package as to be covered"""
        if entry in self.skipped:
            return False
        if not hasattr(package, '__file__'):
            return False
        path = nose.util.src(package.__file__)
        if not path or not path.endswith('.py'):
            return False
        if entry in self.cover_packages:
            return True
        return False

    def finalize(self, result):
        """Set the old standard outputs"""
        self.stopSuite()
        self.stderr.end()
        self.stdout.end()
        if self.fork:
            fork_suite = ncore.XSuite('multiprocess')

            class FakeTest(object):

                def __init__(self, pos):
                    self.pos = pos

                def id(self):
                    return 'nose.multiprocess.success%d' % self.pos

            for i in range(result.testsRun):
                fork_suite.addTest(ncore.XTest(nconst.TEST_SUCCESS, FakeTest(i)))

            for (test, err) in result.errors:
                fork_suite.addTest(ncore.XTest(nconst.TEST_ERROR, test, err=err))

            for (test, err) in result.failures:
                fork_suite.addTest(ncore.XTest(nconst.TEST_FAIL, test, err=err))

            fork_suite.writeXml(self.core_target)