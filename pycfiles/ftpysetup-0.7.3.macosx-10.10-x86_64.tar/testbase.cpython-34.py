# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/ftpysetup/runtest/testbase.py
# Compiled at: 2014-12-30 15:36:44
# Size of source mod 2**32: 9196 bytes
"""Base setuptools command for tests."""
__author__ = ('Lance Finn Helsten', )
__version__ = '0.7.3'
__copyright__ = 'Copyright (C) 2014 Lance Helsten'
__docformat__ = 'reStructuredText en'
__license__ = '\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n'
import sys
if sys.version_info < (3, 0):
    raise Exception('test requires Python 3.0 or higher.')
import os, io, errno, configparser, shutil, itertools
from importlib.abc import Finder, Loader
import re, logging, subprocess, time, unittest
from setuptools.command.test import test as SetupTest
__all__ = [
 'TestBase']
try:
    import coverage
except ImportError:
    print('### Ned Batchelder coverage module missing.', file=sys.stderr)
    print('### Tests will proceed with no coverage report.', file=sys.stderr)

class TestFinder(Finder, Loader):

    def __init__(self, testcommand):
        self.build_lib = testcommand.build_lib
        self.test_lib = testcommand.test_lib

    def find_module(self, fullname, path=None):
        print('-+-+-+-+', fullname, path)

    def load_module(self, fullname):
        pass


class TestBase(SetupTest):

    def initialize_options(self):
        self.suite = []
        self.debug = None
        self.bSetup = False
        self.bTeardown = False
        self.test_type = None
        self.suite_name = None
        self.coverage = False
        self.test_suite = None
        self.test_src = None
        self.build_base = 'build'
        self.build_lib = None
        self.test_base = None
        self.test_lib = None
        self.scripts_base = None

    def finalize_options(self):
        if self.test_type is None:
            raise ValueError('test_type must be set.')
        if self.suite_name is None:
            raise ValueError('suite_name must be set.')
        if self.test_src is None:
            self.test_src = 'test'
        if self.build_lib is None:
            self.build_lib = os.path.join(self.build_base, 'lib')
        if self.test_base is None:
            self.test_base = os.path.join(self.build_base, self.test_type)
        if self.test_lib is None:
            self.test_lib = os.path.join(self.test_base, 'lib')
        if self.scripts_base is None:
            self.scripts_base = os.path.join(self.build_base, 'scripts-{0.version}'.format(sys))
        del sys.path[0]
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        sys.path.insert(0, os.path.abspath(self.build_lib))
        sys.path.insert(0, os.path.abspath(self.test_lib))
        if os.path.isdir(self.test_base):
            shutil.rmtree(self.test_base)
        os.makedirs(self.test_base, exist_ok=True)
        os.makedirs(os.path.join(self.test_base, 'etc'), exist_ok=True)
        for dirpath, dirnames, filenames in os.walk(self.test_src):
            for d in dirnames:
                dst = os.path.join(self.test_lib, dirpath, d)
                if not os.path.exists(dst):
                    os.makedirs(dst, exist_ok=True)
                    continue

            for f in filenames:
                src = os.path.join(dirpath, f)
                dst = os.path.join(self.test_lib, dirpath, f)
                if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                    shutil.copy2(src, dst)
                    continue

        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.NOTSET, filename=os.path.join(self.test_base, 'logfile.log'))
        if self.coverage:
            omit = []
            for dirpath, dirnames, filenames in os.walk(self.test_base):
                omit.append(os.path.join(dirpath, '*.py'))

            for dirpath, dirnames, filenames in os.walk(self.build_lib):
                omit.append(os.path.join(dirpath, '__init__.py'))

            if 'VIRTUAL_ENV' in os.environ:
                for dirpath, dirnames, filenames in os.walk(os.environ['VIRTUAL_ENV']):
                    omit.append(os.path.join(dirpath, '*.py'))

            datafile = os.path.join(self.build_base, 'coverage_data', self.test_type)
            os.makedirs(os.path.dirname(datafile), exist_ok=True)
            self.cov = coverage.coverage(data_file=datafile, data_suffix=True, branch=True, config_file=True, omit=omit)
        else:
            self.cov = NoCoverage()

    def build_test_suite(self):

        def list_tests(suite):
            ret = []
            for t in suite:
                if isinstance(t, unittest.TestSuite):
                    ret.extend(list_tests(t))
                else:
                    ret.append(t)

            return ret

        cacheclear = [i for i in sys.path_importer_cache if os.path.abspath(i).startswith(os.getcwd())]
        for i in cacheclear:
            del sys.path_importer_cache[i]

        if self.suite:
            self.suite = unittest.TestLoader().loadTestsFromName(self.suite)
        else:
            if self.debug:
                self.suite = unittest.TestLoader().loadTestsFromName(self.debug)
                tests = list_tests(self.suite)
                if len(tests) < 1:
                    raise DistutilsArgError('No test case to execute.')
                if len(tests) > 1:
                    raise DistutilsArgError('Only one test case for debug allowed.')
                import importlib
                self.debugModule = importlib.import_module(tests[0].__class__.__module__)
                self.debugClass = getattr(self.debugModule, tests[0].__class__.__name__)
                self.debugSetUp = getattr(self.debugClass, 'setUp')
                self.debugMethod = getattr(self.debugClass, tests[0]._testMethodName)
                self.debugTearDown = getattr(self.debugClass, 'tearDown')
            else:
                self.cov.start()
                self.suite = getattr(__import__('test'), self.suite_name)()
                self.cov.stop()

    def run_test_suite(self):
        if self.debug is None:
            self.cov.start()
            tr = unittest.TextTestRunner()
            tr.run(self.suite)
            self.cov.stop()
            self.cov.save()
            try:
                self.cov.xml_report(outfile=os.path.join(self.build_base, self.test_type + '_coverage.xml'))
                self.cov.html_report(directory=os.path.join(self.build_base, self.test_type + '_htmlcov'))
            except coverage.misc.CoverageException as err:
                pass

        else:
            import pdb
            db = pdb.Pdb()
            db.rcLines.append('import {0.debugModule.__name__}'.format(self))
            if self.bSetup:
                db.rcLines.append('break {0.debugSetUp}'.format(self))
            db.rcLines.append('break {0.debugModule.__name__}.{0.debugClass.__name__}.{0.debugMethod.__name__}'.format(self))
            if self.bTeardown:
                db.rcLines.append('break {0.debugTearDown}'.format(self))
            db.rcLines.append('continue')
            db.rcLines.append('args')
            db.rcLines.append('list')
            db.runcall(self.suite.debug)

    def run(self):
        self.build_test_suite()
        self.run_test_suite()


class NoCoverage:
    __doc__ = 'Class that duck types coverage but does not do anything.'

    def __init__(self, *argv, **kvarg):
        pass

    def analysis(self, morf):
        pass

    def analysis2(self, morf):
        pass

    def annotate(self, morfs=None, directory=None, ignore_errors=None, omit=None, include=None):
        pass

    def clear_exclude(which='exclude'):
        pass

    def combine(self):
        pass

    def erase(self):
        pass

    def exclude(self, regex, which='exclude'):
        pass

    def get_exclude_list(self, which='exclude'):
        pass

    def html_report(self, morfs=None, directory=None, ignore_errors=None, omit=None, include=None):
        pass

    def load(self):
        pass

    def report(self, morfs=None, show_missing=True, ignore_errors=None, file=None, omit=None, include=None):
        pass

    def save(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def sysinfo(self):
        pass

    def use_cache(self):
        pass

    def xml_report(morfs=None, outfile=None, ignore_errors=None, omit=None, include=None):
        pass