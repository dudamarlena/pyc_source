# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/parser/test_parser_js_file.py
# Compiled at: 2017-07-03 15:45:37
# Size of source mod 2**32: 23770 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, tempfile, os, champollion.parser.js_file

def test_get_file_environment_empty(request):
    """Return environment from empty file."""
    file_handle, path = tempfile.mkstemp(suffix='.js')
    os.close(file_handle)
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_file
    @py_assert5 = @py_assert3.fetch_environment
    @py_assert8 = 'path/to/example.js'
    @py_assert10 = 'test.module'
    @py_assert12 = @py_assert5(path, @py_assert8, @py_assert10)
    @py_assert15 = {'id':'path/to/example.js', 
     'module_id':'test.module',  'name':os.path.basename(path),  'path':path,  'content':'',  'description':None,  'class':{},  'function':{},  'data':{},  'export':{},  'import':{}}
    @py_assert14 = @py_assert12 == @py_assert15
    if not @py_assert14:
        @py_format17 = @pytest_ar._call_reprcompare(('==', ), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_file\n}.fetch_environment\n}(%(py7)s, %(py9)s, %(py11)s)\n} == %(py16)s', ), (@py_assert12, @py_assert15)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = None

    def cleanup():
        try:
            os.remove(path)
        except OSError:
            pass

    request.addfinalizer(cleanup)
    return path


@pytest.mark.parametrize(('content', 'expected'),
  [
 ('/**\n * A file description.\n * \n * A detailed description which can be quite long\n * and eventually go over multiple lines.\n *\n * .. note::\n *\n *     A note.\n */\n\nfunction awesomeFunction() {}\n\n',
 'A file description.\n\nA detailed description which can be quite long\nand eventually go over multiple lines.\n\n.. note::\n\n    A note.'),
 ('/**\n * A file description.\n */\n\nfunction awesomeFunction() {}\n\n', 'A file description.'),
 ('/** A file description. */\n\nfunction awesomeFunction() {}\n\n', 'A file description.'),
 ('\n\n// a comment.\n/** A file description. */\n\nfunction awesomeFunction() {}\n\n',
 'A file description.'),
 ('/* a multi-line comment. */\n\n/** A file description. */\n\nfunction awesomeFunction() {}\n\n',
 None),
 ('/**\n A file description.\n \n A detailed description which can be quite long\n and eventually go over multiple lines.\n \n .. note::\n \n     A note.\n*/\n\nfunction awesomeFunction() {}\n\n',
 None)],
  ids=[
 'valid description',
 'valid description on three lines',
 'valid description on one line',
 'valid description with top content',
 'invalid description with incorrect top content',
 'invalid description'])
def test_fetch_file_description(content, expected):
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_file
    @py_assert5 = @py_assert3.fetch_file_description
    @py_assert8 = @py_assert5(content)
    @py_assert10 = @py_assert8 == expected
    if not @py_assert10:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_file\n}.fetch_file_description\n}(%(py7)s)\n} == %(py11)s', ), (@py_assert8, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None


@pytest.mark.parametrize(('environment', 'export_environment', 'expected'),
  [
 (
  {'id':'__identifier__', 
   'description':'A description.', 
   'exported':False, 
   'default':False}, {},
  {'id':'__identifier__', 
   'description':'A description.', 
   'exported':False, 
   'default':False}),
 (
  {'id':'__identifier__', 
   'description':'A description.', 
   'exported':False, 
   'default':False},
  {'__identifier__': {'id':'__identifier__', 
                      'description':'Another description.', 
                      'default':False}},
  {'id':'__identifier__', 
   'description':'A description.', 
   'exported':True, 
   'default':False}),
 (
  {'id':'__identifier__', 
   'description':'A description.', 
   'exported':False, 
   'default':False},
  {'__identifier__': {'id':'__identifier__', 
                      'description':'Another description.', 
                      'default':True}},
  {'id':'__identifier__', 
   'description':'A description.', 
   'exported':True, 
   'default':True}),
 (
  {'id':'__identifier__', 
   'description':None, 
   'exported':False, 
   'default':False},
  {'__identifier__': {'id':'__identifier__', 
                      'description':'Another description.', 
                      'default':False}},
  {'id':'__identifier__', 
   'description':'Another description.', 
   'exported':True, 
   'default':False})],
  ids=[
 'empty export environment',
 'update exported environment',
 'update exported default environment',
 'update description from exported environment'])
def test_update_from_exported_elements(environment, export_environment, expected):
    """Update environment from exported element."""
    champollion.parser.js_file.update_from_exported_elements(environment, export_environment)
    @py_assert1 = environment == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (environment, expected)) % {'py0':@pytest_ar._saferepr(environment) if 'environment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(environment) else 'environment',  'py2':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


@pytest.mark.parametrize(('content', 'expected'),
  [
 (
  'import defaultMember from "module-name"',
  {'test.module.defaultMember': {'id':'test.module.defaultMember', 
                                 'module':'test.module.module-name', 
                                 'name':'defaultMember', 
                                 'alias':None, 
                                 'partial':False}}),
 (
  'import name1 from "./module-name1"\nimport name2 from \'../module-name2\'\n',
  {'test.module.name1':{'id':'test.module.name1', 
    'module':'test.module.module-name1', 
    'name':'name1', 
    'alias':None, 
    'partial':False}, 
   'test.module.name2':{'id':'test.module.name2', 
    'module':'test.module-name2', 
    'name':'name2', 
    'alias':None, 
    'partial':False}}),
 (
  "import {\n    name_1 as alias_1,\n    name_2,\n    name_3,\n} from 'module-name'",
  {'test.module.alias_1':{'id':'test.module.alias_1', 
    'module':'test.module.module-name', 
    'name':'name_1', 
    'alias':'alias_1', 
    'partial':True}, 
   'test.module.name_2':{'id':'test.module.name_2', 
    'module':'test.module.module-name', 
    'name':'name_2', 
    'alias':None, 
    'partial':True}, 
   'test.module.name_3':{'id':'test.module.name_3', 
    'module':'test.module.module-name', 
    'name':'name_3', 
    'alias':None, 
    'partial':True}}),
 (
  'import {name1 as alias1}, name2, {name3} from "./module"\n',
  {'test.module.alias1':{'id':'test.module.alias1', 
    'module':'test.module.module', 
    'name':'name1', 
    'alias':'alias1', 
    'partial':True}, 
   'test.module.name2':{'id':'test.module.name2', 
    'module':'test.module.module', 
    'name':'name2', 
    'alias':None, 
    'partial':False}, 
   'test.module.name3':{'id':'test.module.name3', 
    'module':'test.module.module', 
    'name':'name3', 
    'alias':None, 
    'partial':True}}),
 (
  "import * from 'module1'\nimport * from 'module2'",
  {'test.module.WILDCARD_1':{'id':'test.module.WILDCARD_1', 
    'module':'test.module.module1', 
    'name':'*', 
    'alias':None, 
    'partial':False}, 
   'test.module.WILDCARD_2':{'id':'test.module.WILDCARD_2', 
    'module':'test.module.module2', 
    'name':'*', 
    'alias':None, 
    'partial':False}}),
 (
  "import * as name from 'module'",
  {'test.module.name': {'id':'test.module.name', 
                        'module':'test.module.module', 
                        'name':'*', 
                        'alias':'name', 
                        'partial':False}})],
  ids=[
 'import default from global module',
 'import default from relative module',
 'import partial on several lines with aliases',
 'import default and partial on several lines with aliases',
 'import wildcard',
 'import wildcard with alias'])
def test_fetch_import_environment(content, expected):
    """Return import environment."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_file
    @py_assert5 = @py_assert3.fetch_import_environment
    @py_assert8 = 'test.module'
    @py_assert10 = @py_assert5(content, @py_assert8)
    @py_assert12 = @py_assert10 == expected
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_file\n}.fetch_import_environment\n}(%(py7)s, %(py9)s)\n} == %(py13)s', ), (@py_assert10, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None


@pytest.mark.parametrize(('expression', 'environment', 'wildcards_number', 'expected'),
  [
 (
  'name', None, 0,
  (
   {'module.name': {'id':'module.name', 
                    'module':'test.module', 
                    'name':'name', 
                    'alias':None, 
                    'partial':False}},
   0)),
 (
  '{name}', None, 0,
  (
   {'module.name': {'id':'module.name', 
                    'module':'test.module', 
                    'name':'name', 
                    'alias':None, 
                    'partial':True}},
   0)),
 (
  '{name1 as alias1, name2 as alias2}, name3', None, 1,
  (
   {'module.alias1':{'id':'module.alias1', 
     'module':'test.module', 
     'name':'name1', 
     'alias':'alias1', 
     'partial':True}, 
    'module.alias2':{'id':'module.alias2', 
     'module':'test.module', 
     'name':'name2', 
     'alias':'alias2', 
     'partial':True}, 
    'module.name3':{'id':'module.name3', 
     'module':'test.module', 
     'name':'name3', 
     'alias':None, 
     'partial':False}},
   1)),
 (
  '*', None, 0,
  (
   {'module.WILDCARD_1': {'id':'module.WILDCARD_1', 
                          'module':'test.module', 
                          'name':'*', 
                          'alias':None, 
                          'partial':False}},
   1)),
 (
  '{* as alias}', None, 0,
  (
   {'module.alias': {'id':'module.alias', 
                     'module':'test.module', 
                     'name':'*', 
                     'alias':'alias', 
                     'partial':True}},
   0))],
  ids=[
 'simple default expression',
 'simple partial expression',
 'mixed partial and default binding with aliases',
 'wildcard',
 'aliased wildcard'])
def test_fetch_expression_environment(expression, environment, wildcards_number, expected):
    """Return expression environment."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_file
    @py_assert5 = @py_assert3._fetch_expression_environment
    @py_assert8 = 'module'
    @py_assert10 = 'test.module'
    @py_assert14 = @py_assert5(expression, @py_assert8, @py_assert10, environment, wildcards_number)
    @py_assert16 = @py_assert14 == expected
    if not @py_assert16:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_file\n}._fetch_expression_environment\n}(%(py7)s, %(py9)s, %(py11)s, %(py12)s, %(py13)s)\n} == %(py17)s',), (@py_assert14, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(expression) if 'expression' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expression) else 'expression',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py12':@pytest_ar._saferepr(environment) if 'environment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(environment) else 'environment',  'py13':@pytest_ar._saferepr(wildcards_number) if 'wildcards_number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(wildcards_number) else 'wildcards_number',  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert14 = @py_assert16 = None


@pytest.mark.parametrize(('content', 'expected'),
  [
 (
  '/** a description */\nexport {name}',
  {'test.module.name': {'id':'test.module.name', 
                        'name':'name', 
                        'module':None, 
                        'alias':None, 
                        'partial':True, 
                        'description':'a description', 
                        'default':False, 
                        'line_number':2}}),
 (
  '/** a description */\nexport default name',
  {'test.module.name': {'id':'test.module.name', 
                        'name':'name', 
                        'module':None, 
                        'alias':None, 
                        'partial':False, 
                        'description':'a description', 
                        'default':True, 
                        'line_number':2}}),
 (
  '/** a description */\nexport {name as alias}',
  {'test.module.alias': {'id':'test.module.alias', 
                         'name':'name', 
                         'module':None, 
                         'alias':'alias', 
                         'partial':True, 
                         'description':'a description', 
                         'default':False, 
                         'line_number':2}}),
 (
  '/** a description */\nexport {name1 as alias1, name2 as alias2, name3};',
  {'test.module.alias1':{'id':'test.module.alias1', 
    'name':'name1', 
    'module':None, 
    'alias':'alias1', 
    'partial':True, 
    'description':'a description', 
    'default':False, 
    'line_number':2}, 
   'test.module.alias2':{'id':'test.module.alias2', 
    'name':'name2', 
    'module':None, 
    'alias':'alias2', 
    'partial':True, 
    'description':'a description', 
    'default':False, 
    'line_number':2}, 
   'test.module.name3':{'id':'test.module.name3', 
    'name':'name3', 
    'module':None, 
    'alias':None, 
    'partial':True, 
    'description':'a description', 
    'default':False, 
    'line_number':2}}),
 (
  "/** a description */\nexport name from 'module-name'",
  {'test.module.name': {'id':'test.module.name', 
                        'name':'name', 
                        'module':'test.module.module-name', 
                        'alias':None, 
                        'partial':False, 
                        'description':'a description', 
                        'default':False, 
                        'line_number':2}}),
 (
  '/** a description */\nexport name1 from "./module-name1"\n\n/** another description */\nexport {name2 as alias2} from \'../module-name2\'\n',
  {'test.module.name1':{'id':'test.module.name1', 
    'name':'name1', 
    'module':'test.module.module-name1', 
    'alias':None, 
    'partial':False, 
    'description':'a description', 
    'default':False, 
    'line_number':2}, 
   'test.module.alias2':{'id':'test.module.alias2', 
    'name':'name2', 
    'module':'test.module-name2', 
    'alias':'alias2', 
    'partial':True, 
    'description':'another description', 
    'default':False, 
    'line_number':5}}),
 (
  "export {\n    name_1 as alias_1,\n    name_2,\n    name_3,\n} from 'module-name'",
  {'test.module.alias_1':{'id':'test.module.alias_1', 
    'name':'name_1', 
    'module':'test.module.module-name', 
    'alias':'alias_1', 
    'partial':True, 
    'description':None, 
    'default':False, 
    'line_number':1}, 
   'test.module.name_2':{'id':'test.module.name_2', 
    'name':'name_2', 
    'module':'test.module.module-name', 
    'alias':None, 
    'partial':True, 
    'description':None, 
    'default':False, 
    'line_number':1}, 
   'test.module.name_3':{'id':'test.module.name_3', 
    'name':'name_3', 
    'module':'test.module.module-name', 
    'alias':None, 
    'partial':True, 
    'description':None, 
    'default':False, 
    'line_number':1}})],
  ids=[
 'export simple',
 'export default simple',
 'export simple aliased',
 'export several elements with aliased',
 'export default from global module',
 'export default from relative module',
 'export partial on several lines with aliases'])
def test_fetch_export_environment(content, expected):
    """Return export environment."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_file
    @py_assert5 = @py_assert3.fetch_export_environment
    @py_assert8 = 'test.module'
    @py_assert10 = @py_assert5(content, @py_assert8)
    @py_assert12 = @py_assert10 == expected
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_file\n}.fetch_export_environment\n}(%(py7)s, %(py9)s)\n} == %(py13)s', ), (@py_assert10, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None


@pytest.mark.parametrize(('expression', 'expected'),
  [
 (
  'name;',
  (
   [
    {'id':'test.module.name', 
     'name':'name', 
     'alias':None}],
   0)),
 (
  'name1, name2, name3',
  (
   [
    {'id':'test.module.name1', 
     'name':'name1', 
     'alias':None},
    {'id':'test.module.name2', 
     'name':'name2', 
     'alias':None},
    {'id':'test.module.name3', 
     'name':'name3', 
     'alias':None}],
   0)),
 (
  'name as alias',
  (
   [
    {'id':'test.module.alias', 
     'name':'name', 
     'alias':'alias'}],
   0)),
 (
  'name1, * as name2;',
  (
   [
    {'id':'test.module.name1', 
     'name':'name1', 
     'alias':None},
    {'id':'test.module.name2', 
     'name':'*', 
     'alias':'name2'}],
   0)),
 (
  'connect(mapStateToProps, mapDispatchToProps)(ReactComponent)', ([], 0)),
 (
  'name = 42', ([], 0))],
  ids=[
 'one element',
 'three elements',
 'single element with alias',
 'two elements with wildcard',
 'invalid wrapped element',
 'invalid'])
def test_fetch_binding_environment(expression, expected):
    """Return binding environment."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_file
    @py_assert5 = @py_assert3._fetch_binding_environment
    @py_assert8 = 'test.module'
    @py_assert10 = @py_assert5(expression, @py_assert8)
    @py_assert12 = @py_assert10 == expected
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_file\n}._fetch_binding_environment\n}(%(py7)s, %(py9)s)\n} == %(py13)s', ), (@py_assert10, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(expression) if 'expression' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expression) else 'expression',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None