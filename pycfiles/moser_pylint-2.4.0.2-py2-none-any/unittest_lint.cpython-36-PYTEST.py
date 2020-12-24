# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_lint.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 25301 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, re, sys, tempfile
from contextlib import contextmanager
from importlib import reload
from io import StringIO
from os import chdir, getcwd
from os.path import abspath, basename, dirname, isdir, join, sep
from shutil import rmtree
import pytest, pylint.testutils as testutils
from pylint import checkers, config, exceptions, interfaces, lint
from pylint.checkers.utils import check_messages
from pylint.constants import MSG_STATE_CONFIDENCE, MSG_STATE_SCOPE_CONFIG, MSG_STATE_SCOPE_MODULE
from pylint.exceptions import InvalidMessageError
from pylint.lint import ArgumentPreprocessingError, PyLinter, Run, preprocess_options
from pylint.reporters import text
from pylint.utils import FileState, tokenize_module
if os.name == 'java':
    if os._name == 'nt':
        HOME = 'USERPROFILE'
    else:
        HOME = 'HOME'
else:
    if sys.platform == 'win32':
        HOME = 'USERPROFILE'
    else:
        HOME = 'HOME'
    try:
        PYPY_VERSION_INFO = sys.pypy_version_info
    except AttributeError:
        PYPY_VERSION_INFO = None

    @contextmanager
    def fake_home():
        folder = tempfile.mkdtemp('fake-home')
        old_home = os.environ.get(HOME)
        try:
            os.environ[HOME] = folder
            yield
        finally:
            os.environ.pop('PYLINTRC', '')
            if old_home is None:
                del os.environ[HOME]
            else:
                os.environ[HOME] = old_home
            rmtree(folder, ignore_errors=True)


    def remove(file):
        try:
            os.remove(file)
        except OSError:
            pass


    HERE = abspath(dirname(__file__))
    INPUTDIR = join(HERE, 'input')
    REGRTEST_DATA = join(HERE, 'regrtest_data')

    @contextmanager
    def tempdir():
        """Create a temp directory and change the current location to it.

    This is supposed to be used with a *with* statement.
    """
        tmp = tempfile.mkdtemp()
        current_dir = getcwd()
        chdir(tmp)
        abs_tmp = abspath('.')
        try:
            yield abs_tmp
        finally:
            chdir(current_dir)
            rmtree(abs_tmp)


    def create_files(paths, chroot='.'):
        """Creates directories and files found in <path>.

    :param paths: list of relative paths to files or directories
    :param chroot: the root directory in which paths will be created

    >>> from os.path import isdir, isfile
    >>> isdir('/tmp/a')
    False
    >>> create_files(['a/b/foo.py', 'a/b/c/', 'a/b/c/d/e.py'], '/tmp')
    >>> isdir('/tmp/a')
    True
    >>> isdir('/tmp/a/b/c')
    True
    >>> isfile('/tmp/a/b/c/d/e.py')
    True
    >>> isfile('/tmp/a/b/foo.py')
    True
    """
        dirs, files = set(), set()
        for path in paths:
            path = join(chroot, path)
            filename = basename(path)
            if filename == '':
                dirs.add(path)
            else:
                dirs.add(dirname(path))
                files.add(path)

        for dirpath in dirs:
            if not isdir(dirpath):
                os.makedirs(dirpath)

        for filepath in files:
            open(filepath, 'w').close()


    @pytest.fixture
    def fake_path():
        orig = list(sys.path)
        fake = [1, 2, 3]
        sys.path[:] = fake
        yield fake
        sys.path[:] = orig


    def test_no_args(fake_path):
        with lint.fix_import_path([]):
            @py_assert1 = sys.path
            @py_assert4 = [
             '.']
            @py_assert7 = @py_assert4 + fake_path
            @py_assert3 = @py_assert1 == @py_assert7
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=168)
            if not @py_assert3:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == (%(py5)s + %(py6)s)', ), (@py_assert1, @py_assert7)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4),  'py6':@pytest_ar._saferepr(fake_path) if 'fake_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fake_path) else 'fake_path'}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert3 = @py_assert4 = @py_assert7 = None
        @py_assert1 = sys.path
        @py_assert3 = @py_assert1 == fake_path
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=169)
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, fake_path)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(fake_path) if 'fake_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fake_path) else 'fake_path'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None


    @pytest.mark.parametrize('case', [['a/b/'], ['a/b'], ['a/b/__init__.py'], ['a/'], ['a']])
    def test_one_arg(fake_path, case):
        with tempdir() as (chroot):
            create_files(['a/b/__init__.py'])
            expected = [join(chroot, 'a')] + ['.'] + fake_path
            @py_assert1 = sys.path
            @py_assert3 = @py_assert1 == fake_path
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=180)
            if not @py_assert3:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, fake_path)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(fake_path) if 'fake_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fake_path) else 'fake_path'}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert3 = None
            with lint.fix_import_path(case):
                @py_assert1 = sys.path
                @py_assert3 = @py_assert1 == expected
                if @py_assert3 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=182)
                if not @py_assert3:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert3 = None
            @py_assert1 = sys.path
            @py_assert3 = @py_assert1 == fake_path
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=183)
            if not @py_assert3:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, fake_path)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(fake_path) if 'fake_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fake_path) else 'fake_path'}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert3 = None


    @pytest.mark.parametrize('case', [
     [
      'a/b', 'a/c'],
     [
      'a/c/', 'a/b/'],
     [
      'a/b/__init__.py', 'a/c/__init__.py'],
     [
      'a', 'a/c/__init__.py']])
    def test_two_similar_args(fake_path, case):
        with tempdir() as (chroot):
            create_files(['a/b/__init__.py', 'a/c/__init__.py'])
            expected = [join(chroot, 'a')] + ['.'] + fake_path
            @py_assert1 = sys.path
            @py_assert3 = @py_assert1 == fake_path
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=200)
            if not @py_assert3:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, fake_path)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(fake_path) if 'fake_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fake_path) else 'fake_path'}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert3 = None
            with lint.fix_import_path(case):
                @py_assert1 = sys.path
                @py_assert3 = @py_assert1 == expected
                if @py_assert3 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=202)
                if not @py_assert3:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert3 = None
            @py_assert1 = sys.path
            @py_assert3 = @py_assert1 == fake_path
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=203)
            if not @py_assert3:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, fake_path)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(fake_path) if 'fake_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fake_path) else 'fake_path'}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert3 = None


    @pytest.mark.parametrize('case', [
     [
      'a/b/c/__init__.py', 'a/d/__init__.py', 'a/e/f.py'],
     [
      'a/b/c', 'a', 'a/e'],
     [
      'a/b/c', 'a', 'a/b/c', 'a/e', 'a']])
    def test_more_args(fake_path, case):
        with tempdir() as (chroot):
            create_files(['a/b/c/__init__.py', 'a/d/__init__.py', 'a/e/f.py'])
            expected = [join(chroot, suffix) for suffix in [sep.join(('a', 'b')), 'a', sep.join(('a', 'e'))]] + ['.'] + fake_path
            @py_assert1 = sys.path
            @py_assert3 = @py_assert1 == fake_path
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=226)
            if not @py_assert3:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, fake_path)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(fake_path) if 'fake_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fake_path) else 'fake_path'}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert3 = None
            with lint.fix_import_path(case):
                @py_assert1 = sys.path
                @py_assert3 = @py_assert1 == expected
                if @py_assert3 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=228)
                if not @py_assert3:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert3 = None
            @py_assert1 = sys.path
            @py_assert3 = @py_assert1 == fake_path
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=229)
            if not @py_assert3:
                @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.path\n} == %(py4)s', ), (@py_assert1, fake_path)) % {'py0':@pytest_ar._saferepr(sys) if 'sys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sys) else 'sys',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(fake_path) if 'fake_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fake_path) else 'fake_path'}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert3 = None


    @pytest.fixture(scope='module')
    def disable(disable):
        return ['I']


    @pytest.fixture(scope='module')
    def reporter(reporter):
        return testutils.TestReporter


    @pytest.fixture
    def init_linter(linter):
        linter.open()
        linter.set_current_module('toto')
        linter.file_state = FileState('toto')
        return linter


    def test_pylint_visit_method_taken_in_account(linter):

        class CustomChecker(checkers.BaseChecker):
            __implements__ = interfaces.IAstroidChecker
            name = 'custom'
            msgs = {'W9999': ('', 'custom', '')}

            @check_messages('custom')
            def visit_class(self, _):
                pass

        linter.register_checker(CustomChecker(linter))
        linter.open()
        out = StringIO()
        linter.set_reporter(text.TextReporter(out))
        linter.check('abc')


    def test_enable_message(init_linter):
        linter = init_linter
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=269)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0102'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=270)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        linter.disable('W0101', scope='package')
        linter.disable('W0102', scope='module', line=1)
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=273)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0102'
        @py_assert5 = 1
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=274)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        linter.set_current_module('tutu')
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=276)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0102'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=277)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        linter.enable('W0101', scope='package')
        linter.enable('W0102', scope='module', line=1)
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=280)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0102'
        @py_assert5 = 1
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=281)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


    def test_enable_message_category(init_linter):
        linter = init_linter
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=286)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'C0202'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=287)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        linter.disable('W', scope='package')
        linter.disable('C', scope='module', line=1)
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=290)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'C0202'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=291)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'C0202'
        @py_assert5 = 1
        @py_assert7 = @py_assert1(@py_assert3, line=@py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=292)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, line=%(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        linter.set_current_module('tutu')
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=294)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'C0202'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=295)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        linter.enable('W', scope='package')
        linter.enable('C', scope='module', line=1)
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=298)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'C0202'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=299)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'C0202'
        @py_assert5 = 1
        @py_assert7 = @py_assert1(@py_assert3, line=@py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=300)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, line=%(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


    def test_message_state_scope(init_linter):

        class FakeConfig(object):
            confidence = [
             'HIGH']

        linter = init_linter
        linter.disable('C0202')
        @py_assert3 = linter.get_message_state_scope
        @py_assert5 = 'C0202'
        @py_assert7 = @py_assert3(@py_assert5)
        @py_assert1 = MSG_STATE_SCOPE_CONFIG == @py_assert7
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=309)
        if not @py_assert1:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.get_message_state_scope\n}(%(py6)s)\n}', ), (MSG_STATE_SCOPE_CONFIG, @py_assert7)) % {'py0':@pytest_ar._saferepr(MSG_STATE_SCOPE_CONFIG) if 'MSG_STATE_SCOPE_CONFIG' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MSG_STATE_SCOPE_CONFIG) else 'MSG_STATE_SCOPE_CONFIG',  'py2':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        linter.disable('W0101', scope='module', line=3)
        @py_assert3 = linter.get_message_state_scope
        @py_assert5 = 'C0202'
        @py_assert7 = @py_assert3(@py_assert5)
        @py_assert1 = MSG_STATE_SCOPE_CONFIG == @py_assert7
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=311)
        if not @py_assert1:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.get_message_state_scope\n}(%(py6)s)\n}', ), (MSG_STATE_SCOPE_CONFIG, @py_assert7)) % {'py0':@pytest_ar._saferepr(MSG_STATE_SCOPE_CONFIG) if 'MSG_STATE_SCOPE_CONFIG' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MSG_STATE_SCOPE_CONFIG) else 'MSG_STATE_SCOPE_CONFIG',  'py2':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert3 = linter.get_message_state_scope
        @py_assert5 = 'W0101'
        @py_assert7 = 3
        @py_assert9 = @py_assert3(@py_assert5, @py_assert7)
        @py_assert1 = MSG_STATE_SCOPE_MODULE == @py_assert9
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=312)
        if not @py_assert1:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py10)s\n{%(py10)s = %(py4)s\n{%(py4)s = %(py2)s.get_message_state_scope\n}(%(py6)s, %(py8)s)\n}', ), (MSG_STATE_SCOPE_MODULE, @py_assert9)) % {'py0':@pytest_ar._saferepr(MSG_STATE_SCOPE_MODULE) if 'MSG_STATE_SCOPE_MODULE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MSG_STATE_SCOPE_MODULE) else 'MSG_STATE_SCOPE_MODULE',  'py2':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        linter.enable('W0102', scope='module', line=3)
        @py_assert3 = linter.get_message_state_scope
        @py_assert5 = 'W0102'
        @py_assert7 = 3
        @py_assert9 = @py_assert3(@py_assert5, @py_assert7)
        @py_assert1 = MSG_STATE_SCOPE_MODULE == @py_assert9
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=314)
        if not @py_assert1:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py10)s\n{%(py10)s = %(py4)s\n{%(py4)s = %(py2)s.get_message_state_scope\n}(%(py6)s, %(py8)s)\n}', ), (MSG_STATE_SCOPE_MODULE, @py_assert9)) % {'py0':@pytest_ar._saferepr(MSG_STATE_SCOPE_MODULE) if 'MSG_STATE_SCOPE_MODULE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MSG_STATE_SCOPE_MODULE) else 'MSG_STATE_SCOPE_MODULE',  'py2':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        linter.config = FakeConfig()
        @py_assert3 = linter.get_message_state_scope
        @py_assert5 = 'this-is-bad'
        @py_assert8 = interfaces.INFERENCE
        @py_assert10 = @py_assert3(@py_assert5, confidence=@py_assert8)
        @py_assert1 = MSG_STATE_CONFIDENCE == @py_assert10
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=316)
        if not @py_assert1:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py11)s\n{%(py11)s = %(py4)s\n{%(py4)s = %(py2)s.get_message_state_scope\n}(%(py6)s, confidence=%(py9)s\n{%(py9)s = %(py7)s.INFERENCE\n})\n}', ), (MSG_STATE_CONFIDENCE, @py_assert10)) % {'py0':@pytest_ar._saferepr(MSG_STATE_CONFIDENCE) if 'MSG_STATE_CONFIDENCE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(MSG_STATE_CONFIDENCE) else 'MSG_STATE_CONFIDENCE',  'py2':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(interfaces) if 'interfaces' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interfaces) else 'interfaces',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None


    def test_enable_message_block(init_linter):
        linter = init_linter
        linter.open()
        filepath = join(REGRTEST_DATA, 'func_block_disable_msg.py')
        linter.set_current_module('func_block_disable_msg')
        astroid = linter.get_ast(filepath, 'func_block_disable_msg')
        linter.process_tokens(tokenize_module(astroid))
        fs = linter.file_state
        fs.collect_block_lines(linter.msgs_store, astroid)
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0613'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=331)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=332)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0613'
        @py_assert5 = 13
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=334)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0613'
        @py_assert5 = 18
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=336)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 24
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=338)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 26
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=339)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 32
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=341)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 36
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=342)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 42
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=344)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 43
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=345)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 46
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=346)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 49
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=347)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 51
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=348)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 57
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=350)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 61
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=351)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 64
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=352)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 66
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=353)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E0602'
        @py_assert5 = 57
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=355)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E0602'
        @py_assert5 = 61
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=356)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E0602'
        @py_assert5 = 62
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=357)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E0602'
        @py_assert5 = 64
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=358)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E0602'
        @py_assert5 = 66
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=359)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 70
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=361)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 72
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=362)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 75
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=363)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'E1101'
        @py_assert5 = 77
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=364)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        fs = linter.file_state
        @py_assert0 = 17
        @py_assert3 = fs._suppression_mapping[('W0613', 18)]
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=367)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = 30
        @py_assert3 = fs._suppression_mapping[('E1101', 33)]
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=368)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = ('E1101', 46)
        @py_assert4 = fs._suppression_mapping
        @py_assert2 = @py_assert0 not in @py_assert4
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=369)
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._suppression_mapping\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(fs) if 'fs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(fs) else 'fs',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 1
        @py_assert3 = fs._suppression_mapping[('C0302', 18)]
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=370)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = 1
        @py_assert3 = fs._suppression_mapping[('C0302', 50)]
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=371)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = 106
        @py_assert3 = fs._suppression_mapping[('E1101', 108)]
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=375)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = 109
        @py_assert3 = fs._suppression_mapping[('E1101', 110)]
        @py_assert2 = @py_assert0 == @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=376)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None


    def test_enable_by_symbol(init_linter):
        """messages can be controlled by symbolic names.

    The state is consistent across symbols and numbers.
    """
        linter = init_linter
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=385)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'unreachable'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=386)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0102'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=387)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'dangerous-default-value'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=388)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        linter.disable('unreachable', scope='package')
        linter.disable('dangerous-default-value', scope='module', line=1)
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=391)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'unreachable'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=392)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0102'
        @py_assert5 = 1
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=393)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'dangerous-default-value'
        @py_assert5 = 1
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert9 = not @py_assert7
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=394)
        if not @py_assert9:
            @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        linter.set_current_module('tutu')
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=396)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'unreachable'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=397)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0102'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=398)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'dangerous-default-value'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=399)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        linter.enable('unreachable', scope='package')
        linter.enable('dangerous-default-value', scope='module', line=1)
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0101'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=402)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'unreachable'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=403)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0102'
        @py_assert5 = 1
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=404)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'dangerous-default-value'
        @py_assert5 = 1
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=405)
        if not @py_assert7:
            @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


    def test_enable_report(linter):
        @py_assert1 = linter.report_is_enabled
        @py_assert3 = 'RP0001'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=409)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.report_is_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        linter.disable('RP0001')
        @py_assert1 = linter.report_is_enabled
        @py_assert3 = 'RP0001'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=411)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.report_is_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        linter.enable('RP0001')
        @py_assert1 = linter.report_is_enabled
        @py_assert3 = 'RP0001'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=413)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.report_is_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None


    def test_report_output_format_aliased(linter):
        text.register(linter)
        linter.set_option('output-format', 'text')
        @py_assert1 = linter.reporter
        @py_assert3 = @py_assert1.__class__
        @py_assert5 = @py_assert3.__name__
        @py_assert8 = 'TextReporter'
        @py_assert7 = @py_assert5 == @py_assert8
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=419)
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.reporter\n}.__class__\n}.__name__\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


    def test_set_unsupported_reporter(linter):
        text.register(linter)
        with pytest.raises(exceptions.InvalidReporterError):
            linter.set_option('output-format', 'missing.module.Class')


    def test_set_option_1(linter):
        linter.set_option('disable', 'C0111,W0234')
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'C0111'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=430)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0234'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=431)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0113'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=432)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'missing-docstring'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=433)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'non-iterator-returned'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=434)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


    def test_set_option_2(linter):
        linter.set_option('disable', ('C0111', 'W0234'))
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'C0111'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=439)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0234'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=440)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'W0113'
        @py_assert5 = @py_assert1(@py_assert3)
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=441)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'missing-docstring'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=442)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
        @py_assert1 = linter.is_message_enabled
        @py_assert3 = 'non-iterator-returned'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert7 = not @py_assert5
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=443)
        if not @py_assert7:
            @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.is_message_enabled\n}(%(py4)s)\n}' % {'py0':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


    def test_enable_checkers(linter):
        linter.disable('design')
        @py_assert0 = 'design'
        @py_assert3 = [c.name for c in linter.prepare_checkers()]
        @py_assert2 = @py_assert0 in @py_assert3
        @py_assert7 = not @py_assert2
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=448)
        if not @py_assert7:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format8 = 'assert not %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert7 = None
        linter.enable('design')
        @py_assert0 = 'design'
        @py_assert3 = [c.name for c in linter.prepare_checkers()]
        @py_assert2 = @py_assert0 in @py_assert3
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=450)
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None


    def test_errors_only(linter):
        linter.error_mode()
        checkers = linter.prepare_checkers()
        checker_names = {c.name for c in checkers}
        should_not = {'design', 'format', 'metrics', 'miscellaneous', 'similarities'}
        @py_assert1 = set()
        @py_assert6 = should_not & checker_names
        @py_assert3 = @py_assert1 == @py_assert6
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=458)
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s()\n} == (%(py4)s & %(py5)s)', ), (@py_assert1, @py_assert6)) % {'py0':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(should_not) if 'should_not' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(should_not) else 'should_not',  'py5':@pytest_ar._saferepr(checker_names) if 'checker_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checker_names) else 'checker_names'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert6 = None


    def test_disable_similar(linter):
        linter.set_option('disable', 'RP0801')
        linter.set_option('disable', 'R0801')
        @py_assert0 = 'similarities'
        @py_assert3 = [c.name for c in linter.prepare_checkers()]
        @py_assert2 = @py_assert0 in @py_assert3
        @py_assert7 = not @py_assert2
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=464)
        if not @py_assert7:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format8 = 'assert not %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert7 = None


    def test_disable_alot(linter):
        """check that we disabled a lot of checkers"""
        linter.set_option('reports', False)
        linter.set_option('disable', 'R,C,W')
        checker_names = [c.name for c in linter.prepare_checkers()]
        for cname in ('design', 'metrics', 'similarities'):
            @py_assert1 = cname in checker_names
            @py_assert5 = not @py_assert1
            if @py_assert5 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=473)
            if not @py_assert5:
                @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (cname, checker_names)) % {'py0':@pytest_ar._saferepr(cname) if 'cname' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cname) else 'cname',  'py2':@pytest_ar._saferepr(checker_names) if 'checker_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checker_names) else 'checker_names'}
                @py_format6 = (@pytest_ar._format_assertmsg(cname) + '\n>assert not %(py4)s') % {'py4': @py_format3}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert5 = None


    def test_addmessage(linter):
        linter.set_reporter(testutils.TestReporter())
        linter.open()
        linter.set_current_module('0123')
        linter.add_message('C0301', line=1, args=(1, 2))
        linter.add_message('line-too-long', line=2, args=(3, 4))
        @py_assert0 = ['C:  1: Line too long (1/2)', 'C:  2: Line too long (3/4)']
        @py_assert4 = linter.reporter
        @py_assert6 = @py_assert4.messages
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=482)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.reporter\n}.messages\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


    def test_addmessage_invalid(linter):
        linter.set_reporter(testutils.TestReporter())
        linter.open()
        linter.set_current_module('0123')
        with pytest.raises(InvalidMessageError) as (cm):
            linter.add_message('line-too-long', args=(1, 2))
        @py_assert2 = cm.value
        @py_assert4 = str(@py_assert2)
        @py_assert7 = 'Message C0301 must provide line, got None'
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=495)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(cm) if 'cm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cm) else 'cm',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        with pytest.raises(InvalidMessageError) as (cm):
            linter.add_message('line-too-long', line=2, node='fake_node', args=(1,
                                                                                2))
        @py_assert2 = cm.value
        @py_assert4 = str(@py_assert2)
        @py_assert7 = 'Message C0301 must only provide line, got line=2, node=fake_node'
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=499)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(cm) if 'cm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cm) else 'cm',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        with pytest.raises(InvalidMessageError) as (cm):
            linter.add_message('C0321')
        @py_assert2 = cm.value
        @py_assert4 = str(@py_assert2)
        @py_assert7 = 'Message C0321 must provide Node, got None'
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=506)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.value\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1':@pytest_ar._saferepr(cm) if 'cm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cm) else 'cm',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


    def test_load_plugin_command_line():
        dummy_plugin_path = join(HERE, 'regrtest_data', 'dummy_plugin')
        sys.path.append(dummy_plugin_path)
        run = Run([
         '--load-plugins', 'dummy_plugin', join(HERE, 'regrtest_data', 'empty.py')],
          do_exit=False)
        @py_assert1 = [ch.name for ch in run.linter.get_checkers() if ch.name == 'dummy_plugin']
        @py_assert3 = len(@py_assert1)
        @py_assert6 = 2
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=517)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        sys.path.remove(dummy_plugin_path)


    def test_load_plugin_config_file():
        dummy_plugin_path = join(HERE, 'regrtest_data', 'dummy_plugin')
        sys.path.append(dummy_plugin_path)
        config_path = join(HERE, 'regrtest_data', 'dummy_plugin.rc')
        run = Run([
         '--rcfile', config_path, join(HERE, 'regrtest_data', 'empty.py')],
          do_exit=False)
        @py_assert1 = [ch.name for ch in run.linter.get_checkers() if ch.name == 'dummy_plugin']
        @py_assert3 = len(@py_assert1)
        @py_assert6 = 2
        @py_assert5 = @py_assert3 == @py_assert6
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=534)
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        sys.path.remove(dummy_plugin_path)


    def test_load_plugin_configuration():
        dummy_plugin_path = join(HERE, 'regrtest_data', 'dummy_plugin')
        sys.path.append(dummy_plugin_path)
        run = Run([
         '--load-plugins',
         'dummy_conf_plugin',
         '--ignore',
         'foo,bar',
         join(HERE, 'regrtest_data', 'empty.py')],
          do_exit=False)
        @py_assert1 = run.linter
        @py_assert3 = @py_assert1.config
        @py_assert5 = @py_assert3.black_list
        @py_assert8 = [
         'foo', 'bar', 'bin']
        @py_assert7 = @py_assert5 == @py_assert8
        if @py_assert7 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=556)
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.linter\n}.config\n}.black_list\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(run) if 'run' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(run) else 'run',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


    def test_init_hooks_called_before_load_plugins():
        with pytest.raises(RuntimeError):
            Run(['--load-plugins', 'unexistant', '--init-hook', 'raise RuntimeError'])
        with pytest.raises(RuntimeError):
            Run(['--init-hook', 'raise RuntimeError', '--load-plugins', 'unexistant'])


    def test_analyze_explicit_script(linter):
        linter.set_reporter(testutils.TestReporter())
        linter.check(os.path.join(os.path.dirname(__file__), 'data', 'ascript'))
        @py_assert0 = ['C:  2: Line too long (175/100)']
        @py_assert4 = linter.reporter
        @py_assert6 = @py_assert4.messages
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=569)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.reporter\n}.messages\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(linter) if 'linter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(linter) else 'linter',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


    def test_python3_checker_disabled(linter):
        checker_names = [c.name for c in linter.prepare_checkers()]
        @py_assert0 = 'python3'
        @py_assert2 = @py_assert0 not in checker_names
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=574)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, checker_names)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(checker_names) if 'checker_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checker_names) else 'checker_names'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        linter.set_option('enable', 'python3')
        checker_names = [c.name for c in linter.prepare_checkers()]
        @py_assert0 = 'python3'
        @py_assert2 = @py_assert0 in checker_names
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=578)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, checker_names)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(checker_names) if 'checker_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checker_names) else 'checker_names'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


    def test_full_documentation(linter):
        out = StringIO()
        linter.print_full_documentation(out)
        output = out.getvalue()
        for re_str in ('^Pylint global options and switches$', 'Verbatim name of the checker is ``python3``',
                       '^:old-octal-literal \\(E1608\\):', '^:dummy-variables-rgx:'):
            regexp = re.compile(re_str, re.MULTILINE)
            @py_assert1 = re.search
            @py_assert5 = @py_assert1(regexp, output)
            if @py_assert5 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=596)
            if not @py_assert5:
                @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py3)s, %(py4)s)\n}' % {'py0':@pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(regexp) if 'regexp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(regexp) else 'regexp',  'py4':@pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output',  'py6':@pytest_ar._saferepr(@py_assert5)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert1 = @py_assert5 = None


    @pytest.fixture
    def pop_pylintrc():
        os.environ.pop('PYLINTRC', None)


    @pytest.mark.usefixtures('pop_pylintrc')
    def test_pylint_home():
        uhome = os.path.expanduser('~')
        if uhome == '~':
            expected = '.pylint.d'
        else:
            expected = os.path.join(uhome, '.pylint.d')
        @py_assert1 = config.PYLINT_HOME
        @py_assert3 = @py_assert1 == expected
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=611)
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.PYLINT_HOME\n} == %(py4)s', ), (@py_assert1, expected)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        try:
            pylintd = join(tempfile.gettempdir(), '.pylint.d')
            os.environ['PYLINTHOME'] = pylintd
            try:
                reload(config)
                @py_assert1 = config.PYLINT_HOME
                @py_assert3 = @py_assert1 == pylintd
                if @py_assert3 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=618)
                if not @py_assert3:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.PYLINT_HOME\n} == %(py4)s', ), (@py_assert1, pylintd)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(pylintd) if 'pylintd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pylintd) else 'pylintd'}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert3 = None
            finally:
                try:
                    os.remove(pylintd)
                except:
                    pass

        finally:
            del os.environ['PYLINTHOME']


    @pytest.mark.skipif(PYPY_VERSION_INFO,
      reason="TOX runs this test from within the repo and finds the project's pylintrc.")
    @pytest.mark.usefixtures('pop_pylintrc')
    def test_pylintrc():
        with fake_home():
            current_dir = getcwd()
            chdir(os.path.dirname(os.path.abspath(sys.executable)))
            try:
                @py_assert1 = config.find_pylintrc
                @py_assert3 = @py_assert1()
                @py_assert6 = None
                @py_assert5 = @py_assert3 is @py_assert6
                if @py_assert5 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=639)
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.find_pylintrc\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                os.environ['PYLINTRC'] = join(tempfile.gettempdir(), '.pylintrc')
                @py_assert1 = config.find_pylintrc
                @py_assert3 = @py_assert1()
                @py_assert6 = None
                @py_assert5 = @py_assert3 is @py_assert6
                if @py_assert5 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=641)
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.find_pylintrc\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                os.environ['PYLINTRC'] = '.'
                @py_assert1 = config.find_pylintrc
                @py_assert3 = @py_assert1()
                @py_assert6 = None
                @py_assert5 = @py_assert3 is @py_assert6
                if @py_assert5 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=643)
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.find_pylintrc\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
            finally:
                chdir(current_dir)
                reload(config)


    @pytest.mark.usefixtures('pop_pylintrc')
    def test_pylintrc_parentdir():
        with tempdir() as (chroot):
            create_files([
             'a/pylintrc',
             'a/b/__init__.py',
             'a/b/pylintrc',
             'a/b/c/__init__.py',
             'a/b/c/d/__init__.py',
             'a/b/c/d/e/.pylintrc'])
            with fake_home():
                @py_assert1 = config.find_pylintrc
                @py_assert3 = @py_assert1()
                @py_assert6 = None
                @py_assert5 = @py_assert3 is @py_assert6
                if @py_assert5 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=664)
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.find_pylintrc\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
            results = {'a':join(chroot, 'a', 'pylintrc'),  'a/b':join(chroot, 'a', 'b', 'pylintrc'), 
             'a/b/c':join(chroot, 'a', 'b', 'pylintrc'), 
             'a/b/c/d':join(chroot, 'a', 'b', 'pylintrc'), 
             'a/b/c/d/e':join(chroot, 'a', 'b', 'c', 'd', 'e', '.pylintrc')}
            for basedir, expected in results.items():
                os.chdir(join(chroot, basedir))
                @py_assert1 = config.find_pylintrc
                @py_assert3 = @py_assert1()
                @py_assert5 = @py_assert3 == expected
                if @py_assert5 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=674)
                if not @py_assert5:
                    @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.find_pylintrc\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
                    @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format9))
                @py_assert1 = @py_assert3 = @py_assert5 = None


    @pytest.mark.usefixtures('pop_pylintrc')
    def test_pylintrc_parentdir_no_package():
        with tempdir() as (chroot):
            with fake_home():
                create_files(['a/pylintrc', 'a/b/pylintrc', 'a/b/c/d/__init__.py'])
                @py_assert1 = config.find_pylintrc
                @py_assert3 = @py_assert1()
                @py_assert6 = None
                @py_assert5 = @py_assert3 is @py_assert6
                if @py_assert5 is None:
                    from _pytest.warning_types import PytestWarning
                    from warnings import warn_explicit
                    warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=682)
                if not @py_assert5:
                    @py_format8 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.find_pylintrc\n}()\n} is %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
                    @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format10))
                @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
                results = {'a':join(chroot, 'a', 'pylintrc'), 
                 'a/b':join(chroot, 'a', 'b', 'pylintrc'), 
                 'a/b/c':None, 
                 'a/b/c/d':None}
                for basedir, expected in results.items():
                    os.chdir(join(chroot, basedir))
                    @py_assert1 = config.find_pylintrc
                    @py_assert3 = @py_assert1()
                    @py_assert5 = @py_assert3 == expected
                    if @py_assert5 is None:
                        from _pytest.warning_types import PytestWarning
                        from warnings import warn_explicit
                        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=691)
                    if not @py_assert5:
                        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.find_pylintrc\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
                        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
                        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
                    @py_assert1 = @py_assert3 = @py_assert5 = None


    class TestPreprocessOptions(object):

        def _callback(self, name, value):
            self.args.append((name, value))

        def test_value_equal(self):
            self.args = []
            preprocess_options([
             '--foo', '--bar=baz', '--qu=ux'], {'foo':(
              self._callback, False), 
             'qu':(self._callback, True)})
            @py_assert0 = [
             ('foo', None), ('qu', 'ux')]
            @py_assert4 = self.args
            @py_assert2 = @py_assert0 == @py_assert4
            if @py_assert2 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=704)
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.args\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None

        def test_value_space(self):
            self.args = []
            preprocess_options(['--qu', 'ux'], {'qu': (self._callback, True)})
            @py_assert0 = [('qu', 'ux')]
            @py_assert4 = self.args
            @py_assert2 = @py_assert0 == @py_assert4
            if @py_assert2 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=709)
            if not @py_assert2:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.args\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert0 = @py_assert2 = @py_assert4 = None

        def test_error_missing_expected_value(self):
            with pytest.raises(ArgumentPreprocessingError):
                preprocess_options(['--foo', '--bar', '--qu=ux'], {'bar': (None, True)})
            with pytest.raises(ArgumentPreprocessingError):
                preprocess_options(['--foo', '--bar'], {'bar': (None, True)})

        def test_error_unexpected_value(self):
            with pytest.raises(ArgumentPreprocessingError):
                preprocess_options([
                 '--foo', '--bar=spam', '--qu=ux'], {'bar': (None, False)})


    def test_custom_should_analyze_file():
        """Check that we can write custom should_analyze_file that work
    even for arguments.
    """

        class CustomPyLinter(PyLinter):

            def should_analyze_file(self, modname, path, is_argument=False):
                if os.path.basename(path) == 'wrong.py':
                    return False
                else:
                    return super(CustomPyLinter, self).should_analyze_file(modname,
                      path, is_argument=is_argument)

        package_dir = os.path.join(HERE, 'regrtest_data', 'bad_package')
        wrong_file = os.path.join(package_dir, 'wrong.py')
        for jobs in (1, 2):
            reporter = testutils.TestReporter()
            linter = CustomPyLinter()
            linter.config.jobs = jobs
            linter.config.persistent = 0
            linter.open()
            linter.set_reporter(reporter)
            try:
                sys.path.append(os.path.dirname(package_dir))
                linter.check([package_dir, wrong_file])
            finally:
                sys.path.pop()

            messages = reporter.messages
            @py_assert2 = len(messages)
            @py_assert5 = 1
            @py_assert4 = @py_assert2 == @py_assert5
            if @py_assert4 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=756)
            if not @py_assert4:
                @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(messages) if 'messages' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(messages) else 'messages',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
                @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert2 = @py_assert4 = @py_assert5 = None
            @py_assert0 = 'invalid syntax'
            @py_assert3 = messages[0]
            @py_assert2 = @py_assert0 in @py_assert3
            if @py_assert2 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=757)
            if not @py_assert2:
                @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
                @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert0 = @py_assert2 = @py_assert3 = None


    def test_filename_with__init__(init_linter):
        reporter = testutils.TestReporter()
        linter = init_linter
        linter.open()
        linter.set_reporter(reporter)
        filepath = join(INPUTDIR, 'not__init__.py')
        linter.check([filepath])
        messages = reporter.messages
        @py_assert2 = len(messages)
        @py_assert5 = 0
        @py_assert4 = @py_assert2 == @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_lint.py', lineno=771)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(messages) if 'messages' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(messages) else 'messages',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None