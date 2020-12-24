# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/parser/test_parser_js_module.py
# Compiled at: 2017-07-03 18:39:59
# Size of source mod 2**32: 2607 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, champollion.parser.js_module

def test_get_module_environment_from_file():
    """Return module_id and environment from file id."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_module
    @py_assert5 = @py_assert3.fetch_environment
    @py_assert7 = 'test/module/example.js'
    @py_assert9 = []
    @py_assert11 = @py_assert5(@py_assert7, @py_assert9)
    @py_assert14 = {'id':'test.module.example', 
     'name':'example',  'path':'test/module/example',  'file_id':'test/module/example.js'}
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_module\n}.fetch_environment\n}(%(py8)s, %(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_get_module_environment_from_index_file():
    """Return module_id and environment from index file id."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_module
    @py_assert5 = @py_assert3.fetch_environment
    @py_assert7 = 'test/module/index.js'
    @py_assert9 = []
    @py_assert11 = @py_assert5(@py_assert7, @py_assert9)
    @py_assert14 = {'id':'test.module', 
     'name':'module',  'path':'test/module',  'file_id':'test/module/index.js'}
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_module\n}.fetch_environment\n}(%(py8)s, %(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


def test_get_module_environment_from_file_with_adjacent_index():
    """Return module_id and environment from file id with adjacent index file.
    """
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_module
    @py_assert5 = @py_assert3.fetch_environment
    @py_assert7 = 'test/module/example.js'
    @py_assert9 = [
     'index.js']
    @py_assert11 = @py_assert5(@py_assert7, @py_assert9)
    @py_assert14 = {'id':'test.module.example', 
     'name':'module.example',  'path':'test/module/example',  'file_id':'test/module/example.js'}
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_module\n}.fetch_environment\n}(%(py8)s, %(py10)s)\n} == %(py15)s', ), (@py_assert11, @py_assert14)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None


@pytest.mark.parametrize(('name', 'hierarchy_folders', 'module_names', 'expected'),
  [
 (
  'example',
  [
   'module', 'submodule', 'test'], [],
  'example'),
 (
  'example',
  [
   'module', 'submodule', 'test'],
  [
   'another_module'],
  'example'),
 (
  'example',
  [
   'module', 'submodule', 'test'],
  [
   'module.submodule.test'],
  'module.submodule.test.example'),
 (
  'example',
  [
   'module', 'submodule', 'test'],
  [
   'submodule.test'],
  'submodule.test.example'),
 (
  'example',
  [
   'module', 'submodule', 'test'],
  [
   'another_module', 'submodule.test', 'test'],
  'submodule.test.example')],
  ids=[
 'no module',
 'one module not in hierarchy',
 'one module matching entire hierarchy',
 'one module matching part of the hierarchy',
 'several modules'])
def test_guess_module_name(name, hierarchy_folders, module_names, expected):
    """Return module name from initial name, hierarchy folders and modules."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_module
    @py_assert5 = @py_assert3._guess_module_name
    @py_assert10 = @py_assert5(name, hierarchy_folders, module_names)
    @py_assert12 = @py_assert10 == expected
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_module\n}._guess_module_name\n}(%(py7)s, %(py8)s, %(py9)s)\n} == %(py13)s', ), (@py_assert10, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name',  'py8':@pytest_ar._saferepr(hierarchy_folders) if 'hierarchy_folders' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hierarchy_folders) else 'hierarchy_folders',  'py9':@pytest_ar._saferepr(module_names) if 'module_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module_names) else 'module_names',  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert10 = @py_assert12 = None