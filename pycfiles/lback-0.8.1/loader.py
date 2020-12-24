# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: unittest\loader.pyc
# Compiled at: 2011-03-08 12:43:28
"""Loading unittests."""
import os, re, sys, traceback, types
from functools import cmp_to_key as _CmpToKey
from fnmatch import fnmatch
from . import case, suite
__unittest = True
VALID_MODULE_NAME = re.compile('[_a-z]\\w*\\.py$', re.IGNORECASE)

def _make_failed_import_test(name, suiteClass):
    message = 'Failed to import test module: %s\n%s' % (name, traceback.format_exc())
    return _make_failed_test('ModuleImportFailure', name, ImportError(message), suiteClass)


def _make_failed_load_tests(name, exception, suiteClass):
    return _make_failed_test('LoadTestsFailure', name, exception, suiteClass)


def _make_failed_test(classname, methodname, exception, suiteClass):

    def testFailure(self):
        raise exception

    attrs = {methodname: testFailure}
    TestClass = type(classname, (case.TestCase,), attrs)
    return suiteClass((TestClass(methodname),))


class TestLoader(object):
    """
    This class is responsible for loading tests according to various criteria
    and returning them wrapped in a TestSuite
    """
    testMethodPrefix = 'test'
    sortTestMethodsUsing = cmp
    suiteClass = suite.TestSuite
    _top_level_dir = None

    def loadTestsFromTestCase(self, testCaseClass):
        """Return a suite of all tests cases contained in testCaseClass"""
        if issubclass(testCaseClass, suite.TestSuite):
            raise TypeError('Test cases should not be derived from TestSuite. Maybe you meant to derive from TestCase?')
        testCaseNames = self.getTestCaseNames(testCaseClass)
        if not testCaseNames and hasattr(testCaseClass, 'runTest'):
            testCaseNames = [
             'runTest']
        loaded_suite = self.suiteClass(map(testCaseClass, testCaseNames))
        return loaded_suite

    def loadTestsFromModule(self, module, use_load_tests=True):
        """Return a suite of all tests cases contained in the given module"""
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, case.TestCase):
                tests.append(self.loadTestsFromTestCase(obj))

        load_tests = getattr(module, 'load_tests', None)
        tests = self.suiteClass(tests)
        if use_load_tests and load_tests is not None:
            try:
                return load_tests(self, tests, None)
            except Exception as e:
                return _make_failed_load_tests(module.__name__, e, self.suiteClass)

        return tests

    def loadTestsFromName(self, name, module=None):
        """Return a suite of all tests cases given a string specifier.

        The name may resolve either to a module, a test case class, a
        test method within a test case class, or a callable object which
        returns a TestCase or TestSuite instance.

        The method optionally resolves the names relative to a given module.
        """
        parts = name.split('.')
        if module is None:
            parts_copy = parts[:]
            while parts_copy:
                try:
                    module = __import__(('.').join(parts_copy))
                    break
                except ImportError:
                    del parts_copy[-1]
                    if not parts_copy:
                        raise

            parts = parts[1:]
        obj = module
        for part in parts:
            parent, obj = obj, getattr(obj, part)

        if isinstance(obj, types.ModuleType):
            return self.loadTestsFromModule(obj)
        else:
            if isinstance(obj, type) and issubclass(obj, case.TestCase):
                return self.loadTestsFromTestCase(obj)
            if isinstance(obj, types.UnboundMethodType) and isinstance(parent, type) and issubclass(parent, case.TestCase):
                return self.suiteClass([parent(obj.__name__)])
            if isinstance(obj, suite.TestSuite):
                return obj
            if hasattr(obj, '__call__'):
                test = obj()
                if isinstance(test, suite.TestSuite):
                    return test
                if isinstance(test, case.TestCase):
                    return self.suiteClass([test])
                raise TypeError('calling %s returned %s, not a test' % (
                 obj, test))
            else:
                raise TypeError("don't know how to make test from: %s" % obj)
            return

    def loadTestsFromNames(self, names, module=None):
        """Return a suite of all tests cases found using the given sequence
        of string specifiers. See 'loadTestsFromName()'.
        """
        suites = [ self.loadTestsFromName(name, module) for name in names ]
        return self.suiteClass(suites)

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """

        def isTestMethod(attrname, testCaseClass=testCaseClass, prefix=self.testMethodPrefix):
            return attrname.startswith(prefix) and hasattr(getattr(testCaseClass, attrname), '__call__')

        testFnNames = filter(isTestMethod, dir(testCaseClass))
        if self.sortTestMethodsUsing:
            testFnNames.sort(key=_CmpToKey(self.sortTestMethodsUsing))
        return testFnNames

    def discover(self, start_dir, pattern='test*.py', top_level_dir=None):
        """Find and return all test modules from the specified start
        directory, recursing into subdirectories to find them. Only test files
        that match the pattern will be loaded. (Using shell style pattern
        matching.)

        All test modules must be importable from the top level of the project.
        If the start directory is not the top level directory then the top
        level directory must be specified separately.

        If a test package name (directory with '__init__.py') matches the
        pattern then the package will be checked for a 'load_tests' function. If
        this exists then it will be called with loader, tests, pattern.

        If load_tests exists then discovery does  *not* recurse into the package,
        load_tests is responsible for loading all tests in the package.

        The pattern is deliberately not stored as a loader attribute so that
        packages can continue discovery themselves. top_level_dir is stored so
        load_tests does not need to pass this argument in to loader.discover().
        """
        set_implicit_top = False
        if top_level_dir is None and self._top_level_dir is not None:
            top_level_dir = self._top_level_dir
        else:
            if top_level_dir is None:
                set_implicit_top = True
                top_level_dir = start_dir
            top_level_dir = os.path.abspath(top_level_dir)
            if top_level_dir not in sys.path:
                sys.path.insert(0, top_level_dir)
            self._top_level_dir = top_level_dir
            is_not_importable = False
            if os.path.isdir(os.path.abspath(start_dir)):
                start_dir = os.path.abspath(start_dir)
                if start_dir != top_level_dir:
                    is_not_importable = not os.path.isfile(os.path.join(start_dir, '__init__.py'))
            else:
                try:
                    __import__(start_dir)
                except ImportError:
                    is_not_importable = True

                the_module = sys.modules[start_dir]
                top_part = start_dir.split('.')[0]
                start_dir = os.path.abspath(os.path.dirname(the_module.__file__))
                if set_implicit_top:
                    self._top_level_dir = self._get_directory_containing_module(top_part)
                    sys.path.remove(top_level_dir)
        if is_not_importable:
            raise ImportError('Start directory is not importable: %r' % start_dir)
        tests = list(self._find_tests(start_dir, pattern))
        return self.suiteClass(tests)

    def _get_directory_containing_module(self, module_name):
        module = sys.modules[module_name]
        full_path = os.path.abspath(module.__file__)
        if os.path.basename(full_path).lower().startswith('__init__.py'):
            return os.path.dirname(os.path.dirname(full_path))
        else:
            return os.path.dirname(full_path)

    def _get_name_from_path--- This code section failed: ---

 L. 220         0  LOAD_GLOBAL           0  'os'
                3  LOAD_ATTR             1  'path'
                6  LOAD_ATTR             2  'splitext'
                9  LOAD_GLOBAL           0  'os'
               12  LOAD_ATTR             1  'path'
               15  LOAD_ATTR             3  'normpath'
               18  LOAD_FAST             1  'path'
               21  CALL_FUNCTION_1       1  None
               24  CALL_FUNCTION_1       1  None
               27  LOAD_CONST               0
               30  BINARY_SUBSCR    
               31  STORE_FAST            1  'path'

 L. 222        34  LOAD_GLOBAL           0  'os'
               37  LOAD_ATTR             1  'path'
               40  LOAD_ATTR             4  'relpath'
               43  LOAD_FAST             1  'path'
               46  LOAD_FAST             0  'self'
               49  LOAD_ATTR             5  '_top_level_dir'
               52  CALL_FUNCTION_2       2  None
               55  STORE_FAST            2  '_relpath'

 L. 223        58  LOAD_GLOBAL           0  'os'
               61  LOAD_ATTR             1  'path'
               64  LOAD_ATTR             6  'isabs'
               67  LOAD_FAST             2  '_relpath'
               70  CALL_FUNCTION_1       1  None
               73  UNARY_NOT        
               74  POP_JUMP_IF_TRUE     86  'to 86'
               77  LOAD_ASSERT              AssertionError
               80  LOAD_CONST               'Path must be within the project'
               83  RAISE_VARARGS_2       2  None

 L. 224        86  LOAD_FAST             2  '_relpath'
               89  LOAD_ATTR             8  'startswith'
               92  LOAD_CONST               '..'
               95  CALL_FUNCTION_1       1  None
               98  UNARY_NOT        
               99  POP_JUMP_IF_TRUE    111  'to 111'
              102  LOAD_ASSERT              AssertionError
              105  LOAD_CONST               'Path must be within the project'
              108  RAISE_VARARGS_2       2  None

 L. 226       111  LOAD_FAST             2  '_relpath'
              114  LOAD_ATTR             9  'replace'
              117  LOAD_GLOBAL           0  'os'
              120  LOAD_ATTR             1  'path'
              123  LOAD_ATTR            10  'sep'
              126  LOAD_CONST               '.'
              129  CALL_FUNCTION_2       2  None
              132  STORE_FAST            3  'name'

 L. 227       135  LOAD_FAST             3  'name'
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 138

    def _get_module_from_name(self, name):
        __import__(name)
        return sys.modules[name]

    def _match_path(self, path, full_path, pattern):
        return fnmatch(path, pattern)

    def _find_tests(self, start_dir, pattern):
        """Used by discovery. Yields test suites it loads."""
        paths = os.listdir(start_dir)
        for path in paths:
            full_path = os.path.join(start_dir, path)
            if os.path.isfile(full_path):
                if not VALID_MODULE_NAME.match(path):
                    continue
                if not self._match_path(path, full_path, pattern):
                    continue
                name = self._get_name_from_path(full_path)
                try:
                    module = self._get_module_from_name(name)
                except:
                    yield _make_failed_import_test(name, self.suiteClass)
                else:
                    mod_file = os.path.abspath(getattr(module, '__file__', full_path))
                    realpath = os.path.splitext(mod_file)[0]
                    fullpath_noext = os.path.splitext(full_path)[0]
                    if realpath.lower() != fullpath_noext.lower():
                        module_dir = os.path.dirname(realpath)
                        mod_name = os.path.splitext(os.path.basename(full_path))[0]
                        expected_dir = os.path.dirname(full_path)
                        msg = '%r module incorrectly imported from %r. Expected %r. Is this module globally installed?'
                        raise ImportError(msg % (mod_name, module_dir, expected_dir))
                    yield self.loadTestsFromModule(module)

            elif os.path.isdir(full_path):
                if not os.path.isfile(os.path.join(full_path, '__init__.py')):
                    continue
                load_tests = None
                tests = None
                if fnmatch(path, pattern):
                    name = self._get_name_from_path(full_path)
                    package = self._get_module_from_name(name)
                    load_tests = getattr(package, 'load_tests', None)
                    tests = self.loadTestsFromModule(package, use_load_tests=False)
                if load_tests is None:
                    if tests is not None:
                        yield tests
                    for test in self._find_tests(full_path, pattern):
                        yield test

                else:
                    try:
                        yield load_tests(self, tests, pattern)
                    except Exception as e:
                        yield _make_failed_load_tests(package.__name__, e, self.suiteClass)

        return


defaultTestLoader = TestLoader()

def _makeLoader(prefix, sortUsing, suiteClass=None):
    loader = TestLoader()
    loader.sortTestMethodsUsing = sortUsing
    loader.testMethodPrefix = prefix
    if suiteClass:
        loader.suiteClass = suiteClass
    return loader


def getTestCaseNames(testCaseClass, prefix, sortUsing=cmp):
    return _makeLoader(prefix, sortUsing).getTestCaseNames(testCaseClass)


def makeSuite(testCaseClass, prefix='test', sortUsing=cmp, suiteClass=suite.TestSuite):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromTestCase(testCaseClass)


def findTestCases(module, prefix='test', sortUsing=cmp, suiteClass=suite.TestSuite):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromModule(module)