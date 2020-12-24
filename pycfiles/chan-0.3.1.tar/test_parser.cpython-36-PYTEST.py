# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/parser/test_parser.py
# Compiled at: 2017-06-11 15:30:19
# Size of source mod 2**32: 599 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, champollion.parser

def test_get_environment_error():
    """Raise an error if the path is incorrect."""
    with pytest.raises(OSError):
        champollion.parser.fetch_environment('')


def test_get_environment_empty(temporary_directory):
    """Return an empty environment."""
    environment = {'module':{},  'class':{},  'method':{},  'attribute':{},  'function':{},  'data':{},  'file':{}}
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.fetch_environment
    @py_assert6 = @py_assert3(temporary_directory)
    @py_assert8 = @py_assert6 == environment
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.fetch_environment\n}(%(py5)s)\n} == %(py9)s', ), (@py_assert6, environment)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(temporary_directory) if 'temporary_directory' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(temporary_directory) else 'temporary_directory',  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(environment) if 'environment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(environment) else 'environment'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None