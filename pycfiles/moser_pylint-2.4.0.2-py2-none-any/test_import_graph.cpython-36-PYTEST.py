# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/test_import_graph.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 2347 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from os.path import exists
import pytest, pylint.testutils as testutils
from pylint.checkers import imports, initialize
from pylint.lint import PyLinter

@pytest.fixture
def dest():
    dest = 'dependencies_graph.dot'
    yield dest
    os.remove(dest)


def test_dependencies_graph(dest):
    imports._dependencies_graph(dest, {'labas':['hoho', 'yep'],  'hoho':['yep']})
    with open(dest) as (stream):
        @py_assert1 = stream.read
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3.strip
        @py_assert7 = @py_assert5()
        @py_assert10 = '\ndigraph "dependencies_graph" {\nrankdir=LR\ncharset="utf-8"\nURL="." node[shape="box"]\n"hoho" [];\n"yep" [];\n"labas" [];\n"yep" -> "hoho" [];\n"hoho" -> "labas" [];\n"yep" -> "labas" [];\n}\n'
        @py_assert12 = @py_assert10.strip
        @py_assert14 = @py_assert12()
        @py_assert9 = @py_assert7 == @py_assert14
        if @py_assert9 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_import_graph.py', lineno=32)
        if not @py_assert9:
            @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n}.strip\n}()\n} == %(py15)s\n{%(py15)s = %(py13)s\n{%(py13)s = %(py11)s.strip\n}()\n}', ), (@py_assert7, @py_assert14)) % {'py0':@pytest_ar._saferepr(stream) if 'stream' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(stream) else 'stream',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
            @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
            raise AssertionError(@pytest_ar._format_explanation(@py_format18))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = @py_assert12 = @py_assert14 = None


@pytest.fixture
def linter():
    l = PyLinter(reporter=(testutils.TestReporter()))
    initialize(l)
    return l


@pytest.fixture
def remove_files():
    yield
    for fname in ('import.dot', 'ext_import.dot', 'int_import.dot'):
        try:
            os.remove(fname)
        except:
            pass


@pytest.mark.usefixtures('remove_files')
def test_checker_dep_graphs(linter):
    l = linter
    l.global_set_option('persistent', False)
    l.global_set_option('reports', True)
    l.global_set_option('enable', 'imports')
    l.global_set_option('import-graph', 'import.dot')
    l.global_set_option('ext-import-graph', 'ext_import.dot')
    l.global_set_option('int-import-graph', 'int_import.dot')
    l.global_set_option('int-import-graph', 'int_import.dot')
    l.global_set_option('ignore', ('func_unknown_encoding.py', ))
    l.check('input')
    l.generate_reports()
    @py_assert1 = 'import.dot'
    @py_assert3 = exists(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_import_graph.py', lineno=81)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(exists) if 'exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exists) else 'exists',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = 'ext_import.dot'
    @py_assert3 = exists(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_import_graph.py', lineno=82)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(exists) if 'exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exists) else 'exists',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = 'int_import.dot'
    @py_assert3 = exists(@py_assert1)
    if @py_assert3 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/test_import_graph.py', lineno=83)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(exists) if 'exists' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(exists) else 'exists',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None