# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/test_regr.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 4078 bytes
"""non regression tests for pylint, which requires a too specific configuration
to be incorporated in the automatic functional test framework
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
from os.path import abspath, dirname, join
import astroid, pytest, pylint.testutils as testutils
REGR_DATA = join(dirname(abspath(__file__)), 'regrtest_data')
sys.path.insert(1, REGR_DATA)
try:
    PYPY_VERSION_INFO = sys.pypy_version_info
except AttributeError:
    PYPY_VERSION_INFO = None

@pytest.fixture(scope='module')
def reporter(reporter):
    return testutils.TestReporter


@pytest.fixture(scope='module')
def disable(disable):
    return ['I']


@pytest.fixture
def finalize_linter(linter):
    """call reporter.finalize() to cleanup
    pending messages if a test finished badly
    """
    yield linter
    linter.reporter.finalize()


def Equals(expected):
    return lambda got: got == expected


@pytest.mark.parametrize('file_name, check', [
 (
  'package.__init__', Equals('')),
 (
  'precedence_test', Equals('')),
 (
  'import_package_subpackage_module', Equals('')),
 (
  'pylint.checkers.__init__', lambda x: '__path__' not in x),
 (
  join(REGR_DATA, 'classdoc_usage.py'), Equals('')),
 (
  join(REGR_DATA, 'module_global.py'), Equals('')),
 (
  join(REGR_DATA, 'decimal_inference.py'), Equals('')),
 (
  join(REGR_DATA, 'absimp', 'string.py'), Equals('')),
 (
  join(REGR_DATA, 'bad_package'), lambda x: 'Unused import missing' in x)])
def test_package(finalize_linter, file_name, check):
    finalize_linter.check(file_name)
    got = finalize_linter.reporter.finalize().strip()
    @py_assert2 = check(got)
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_regr.py', lineno=75)
    if not @py_assert2:
        @py_format4 = 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}' % {'py0':@pytest_ar._saferepr(check) if 'check' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check) else 'check',  'py1':@pytest_ar._saferepr(got) if 'got' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(got) else 'got',  'py3':@pytest_ar._saferepr(@py_assert2)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None


@pytest.mark.parametrize('file_name', [
 join(REGR_DATA, 'import_assign.py'),
 join(REGR_DATA, 'special_attr_scope_lookup_crash.py'),
 join(REGR_DATA, 'try_finally_disable_msg_crash')])
def test_crash(finalize_linter, file_name):
    finalize_linter.check(file_name)


@pytest.mark.parametrize('fname', [x for x in os.listdir(REGR_DATA) if x.endswith('_crash.py')])
def test_descriptor_crash(fname, finalize_linter):
    finalize_linter.check(join(REGR_DATA, fname))
    finalize_linter.reporter.finalize().strip()


@pytest.fixture
def modify_path():
    cwd = os.getcwd()
    sys.path.insert(0, '')
    yield
    sys.path.pop(0)
    os.chdir(cwd)


@pytest.mark.usefixtures('modify_path')
def test_check_package___init__(finalize_linter):
    filename = 'package.__init__'
    finalize_linter.check(filename)
    checked = list(finalize_linter.stats['by_module'].keys())
    @py_assert2 = [filename]
    @py_assert1 = checked == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_regr.py', lineno=112)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (checked, @py_assert2)) % {'py0':@pytest_ar._saferepr(checked) if 'checked' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checked) else 'checked',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    os.chdir(join(REGR_DATA, 'package'))
    finalize_linter.check('__init__')
    checked = list(finalize_linter.stats['by_module'].keys())
    @py_assert2 = ['__init__']
    @py_assert1 = checked == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_regr.py', lineno=117)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (checked, @py_assert2)) % {'py0':@pytest_ar._saferepr(checked) if 'checked' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checked) else 'checked',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_pylint_config_attr():
    mod = astroid.MANAGER.ast_from_module_name('pylint.lint')
    pylinter = mod['PyLinter']
    expect = [
     'OptionsManagerMixIn',
     'object',
     'MessagesHandlerMixIn',
     'ReportsHandlerMixIn',
     'BaseTokenChecker',
     'BaseChecker',
     'OptionsProviderMixIn']
    @py_assert0 = [c.name for c in pylinter.ancestors()]
    @py_assert2 = @py_assert0 == expect
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_regr.py', lineno=132)
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, expect)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(expect) if 'expect' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expect) else 'expect'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = astroid.Instance
    @py_assert5 = @py_assert2(pylinter)
    @py_assert7 = @py_assert5.getattr
    @py_assert9 = 'config'
    @py_assert11 = @py_assert7(@py_assert9)
    @py_assert13 = list(@py_assert11)
    if @py_assert13 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_regr.py', lineno=133)
    if not @py_assert13:
        @py_format15 = 'assert %(py14)s\n{%(py14)s = %(py0)s(%(py12)s\n{%(py12)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py3)s\n{%(py3)s = %(py1)s.Instance\n}(%(py4)s)\n}.getattr\n}(%(py10)s)\n})\n}' % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(astroid) if 'astroid' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(astroid) else 'astroid',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(pylinter) if 'pylinter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pylinter) else 'pylinter',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    inferred = list(astroid.Instance(pylinter).igetattr('config'))
    @py_assert2 = len(inferred)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_regr.py', lineno=135)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(inferred) if 'inferred' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inferred) else 'inferred',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = inferred[0]
    @py_assert2 = @py_assert0.root
    @py_assert4 = @py_assert2()
    @py_assert6 = @py_assert4.name
    @py_assert9 = 'optparse'
    @py_assert8 = @py_assert6 == @py_assert9
    if @py_assert8 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_regr.py', lineno=136)
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.root\n}()\n}.name\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert0 = inferred[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'Values'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_regr.py', lineno=137)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None