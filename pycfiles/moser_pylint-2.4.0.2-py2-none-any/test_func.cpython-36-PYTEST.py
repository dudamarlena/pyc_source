# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/test_func.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 4781 bytes
"""functional/non regression tests for pylint"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, re, sys
from os.path import abspath, dirname, join
import pytest
from pylint.testutils import _get_tests_info, linter
PY3K = sys.version_info >= (3, 0)
SYS_VERS_STR = '%d%d%d' % sys.version_info[:3]
INPUT_DIR = join(dirname(abspath(__file__)), 'input')
MSG_DIR = join(dirname(abspath(__file__)), 'messages')
FILTER_RGX = None
UPDATE = False
INFO_TEST_RGX = re.compile('^func_i\\d\\d\\d\\d$')
quote = "'" if sys.version_info >= (3, 3) else ''

def exception_str(self, ex):
    """function used to replace default __str__ method of exception instances"""
    return 'in %s\n:: %s' % (ex.file, ', '.join(ex.args))


class LintTestUsingModule(object):
    INPUT_DIR = None
    DEFAULT_PACKAGE = 'input'
    package = DEFAULT_PACKAGE
    linter = linter
    module = None
    depends = None
    output = None
    _TEST_TYPE = 'module'

    def _test_functionality(self):
        tocheck = [
         self.package + '.' + self.module]
        if self.depends:
            tocheck += [self.package + '.%s' % name.replace('.py', '') for name, _ in self.depends]
        self._test(tocheck)

    def _check_result(self, got):
        @py_assert1 = self._get_expected
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3.strip
        @py_assert7 = @py_assert5()
        @py_assert9 = '\n'
        @py_assert11 = @py_assert7 + @py_assert9
        @py_assert14 = got.strip
        @py_assert16 = @py_assert14()
        @py_assert18 = '\n'
        @py_assert20 = @py_assert16 + @py_assert18
        @py_assert12 = @py_assert11 == @py_assert20
        if @py_assert12 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_func.py', lineno=70)
        if not @py_assert12:
            @py_format21 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s._get_expected\n}()\n}.strip\n}()\n} + %(py10)s) == (%(py17)s\n{%(py17)s = %(py15)s\n{%(py15)s = %(py13)s.strip\n}()\n} + %(py19)s)', ), (@py_assert11, @py_assert20)) % {'py0':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(got) if 'got' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(got) else 'got',  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(@py_assert18)}
            @py_format23 = 'assert %(py22)s' % {'py22': @py_format21}
            raise AssertionError(@pytest_ar._format_explanation(@py_format23))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = None

    def _test(self, tocheck):
        if INFO_TEST_RGX.match(self.module):
            self.linter.enable('I')
        else:
            self.linter.disable('I')
        try:
            self.linter.check(tocheck)
        except Exception as ex:
            self.linter.reporter.finalize()
            ex.file = tocheck
            print(ex)
            ex.__str__ = exception_str
            raise

        self._check_result(self.linter.reporter.finalize())

    def _has_output(self):
        return not self.module.startswith('func_noerror_')

    def _get_expected(self):
        if self._has_output():
            if self.output:
                with open(self.output, 'r') as (fobj):
                    return fobj.read().strip() + '\n'
        else:
            return ''


class LintTestUpdate(LintTestUsingModule):
    _TEST_TYPE = 'update'

    def _check_result(self, got):
        if self._has_output():
            try:
                expected = self._get_expected()
            except IOError:
                expected = ''

            if got != expected:
                with open(self.output, 'w') as (fobj):
                    fobj.write(got)


def gen_tests(filter_rgx):
    if filter_rgx:
        is_to_run = re.compile(filter_rgx).search
    else:
        is_to_run = lambda x: 1
    tests = []
    for module_file, messages_file in _get_tests_info(INPUT_DIR, MSG_DIR, 'func_', ''):
        if not not is_to_run(module_file):
            if module_file.endswith(('.pyc', '$py.class')):
                pass
            else:
                base = module_file.replace('.py', '').split('_')[1]
                dependencies = _get_tests_info(INPUT_DIR, MSG_DIR, base, '.py')
                tests.append((module_file, messages_file, dependencies))

    if UPDATE:
        return tests
    else:
        @py_assert2 = len(tests)
        @py_assert5 = 196
        @py_assert4 = @py_assert2 < @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_func.py', lineno=130)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('<', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} < %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(tests) if 'tests' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tests) else 'tests',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg('Please do not add new test cases here.') + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        return tests


@pytest.mark.parametrize('module_file,messages_file,dependencies',
  (gen_tests(FILTER_RGX)),
  ids=[o[0] for o in gen_tests(FILTER_RGX)])
def test_functionality(module_file, messages_file, dependencies):
    LT = LintTestUpdate() if UPDATE else LintTestUsingModule()
    LT.module = module_file.replace('.py', '')
    LT.output = messages_file
    LT.depends = dependencies or None
    LT.INPUT_DIR = INPUT_DIR
    LT._test_functionality()


if __name__ == '__main__':
    if '-u' in sys.argv:
        UPDATE = True
        sys.argv.remove('-u')
    if len(sys.argv) > 1:
        FILTER_RGX = sys.argv[1]
        del sys.argv[1]
    pytest.main(sys.argv)