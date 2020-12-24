# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/acceptance/test_stdlib.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1317 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, contextlib, io, os, sys, pytest, pylint.lint

def is_module(filename):
    return filename.endswith('.py')


def is_package(filename, location):
    return os.path.exists(os.path.join(location, filename, '__init__.py'))


@contextlib.contextmanager
def _patch_stdout(out):
    sys.stdout = out
    try:
        yield
    finally:
        sys.stdout = sys.__stdout__


LIB_DIRS = [
 os.path.dirname(os.__file__)]
MODULES_TO_CHECK = [(location, module) for location in LIB_DIRS for module in os.listdir(location) if is_module(module) or is_package(module, location)]
MODULES_NAMES = [m[1] for m in MODULES_TO_CHECK]

@pytest.mark.acceptance
@pytest.mark.parametrize(('test_module_location', 'test_module_name'),
  MODULES_TO_CHECK, ids=MODULES_NAMES)
def test_libmodule(test_module_location, test_module_name):
    os.chdir(test_module_location)
    with _patch_stdout(io.StringIO()):
        try:
            pylint.lint.Run([test_module_name, '--enable=all', '--ignore=test'])
        except SystemExit as ex:
            @py_assert1 = ex.code
            @py_assert4 = 32
            @py_assert3 = @py_assert1 != @py_assert4
            if @py_assert3 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/acceptance/test_stdlib.py', lineno=51)
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('!=', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.code\n} != %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(ex) if 'ex' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ex) else 'ex',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None
            return

        @py_assert0 = False
        if @py_assert0 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/acceptance/test_stdlib.py', lineno=54)
        if not @py_assert0:
            @py_format2 = (@pytest_ar._format_assertmsg("shouldn't get there") + '\n>assert %(py1)s') % {'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format2))
        @py_assert0 = None