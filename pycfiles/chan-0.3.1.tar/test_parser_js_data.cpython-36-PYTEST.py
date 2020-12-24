# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/parser/test_parser_js_data.py
# Compiled at: 2017-07-02 17:02:10
# Size of source mod 2**32: 5909 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, champollion.parser.js_data

@pytest.mark.parametrize(('content', 'expected'),
  [
 (
  '/**\n * test dictionary data.\n * \n * Detailed description.\n */\nexport const DATA = 42;\n',
  {'test.module.DATA': {'id':'test.module.DATA', 
                        'module_id':'test.module', 
                        'exported':True, 
                        'default':False, 
                        'name':'DATA', 
                        'type':'const', 
                        'value':'42', 
                        'line_number':6, 
                        'description':'test dictionary data.\n\nDetailed description.'}}),
 (
  'export default var DATA = {\n   key1: value1,\n   key2: value2,\n   key3: value3,\n};\n',
  {'test.module.DATA': {'id':'test.module.DATA', 
                        'module_id':'test.module', 
                        'exported':True, 
                        'default':True, 
                        'name':'DATA', 
                        'type':'var', 
                        'value':'{ key1: value1, key2: value2, key3: value3, }', 
                        'line_number':1, 
                        'description':None}}),
 (
  '/** test list data */\nlet DATA = [\n    1, 2, 3 ];\n',
  {'test.module.DATA': {'id':'test.module.DATA', 
                        'module_id':'test.module', 
                        'exported':False, 
                        'default':False, 
                        'name':'DATA', 
                        'type':'let', 
                        'value':'[ 1, 2, 3 ]', 
                        'line_number':2, 
                        'description':'test list data'}}),
 (
  'let DATA = arg =>\n    console.log(arg);\n',
  {'test.module.DATA': {'id':'test.module.DATA', 
                        'module_id':'test.module', 
                        'exported':False, 
                        'default':False, 
                        'name':'DATA', 
                        'type':'let', 
                        'value':'arg =>console.log(arg)', 
                        'line_number':1, 
                        'description':None}}),
 (
  'const SUM = (arg1, arg2) => {\n    return arg1 + arg2;\n};',
  {'test.module.SUM': {'id':'test.module.SUM', 
                       'module_id':'test.module', 
                       'exported':False, 
                       'default':False, 
                       'name':'SUM', 
                       'type':'const', 
                       'value':'(arg1, arg2) => { return arg1 + arg2; }', 
                       'line_number':1, 
                       'description':None}})],
  ids=[
 'valid data',
 'valid object data',
 'valid list data',
 'valid arrow-type function with single argument',
 'valid arrow-type function with severak arguments'])
def test_get_data_environment(content, expected):
    """Return data environment from content."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_data
    @py_assert5 = @py_assert3.fetch_environment
    @py_assert8 = 'test.module'
    @py_assert10 = @py_assert5(content, @py_assert8)
    @py_assert12 = @py_assert10 == expected
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_data\n}.fetch_environment\n}(%(py7)s, %(py9)s)\n} == %(py13)s', ), (@py_assert10, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None


@pytest.mark.parametrize(('content', 'expected'),
  [
 (
  'const data_test = 42;',
  {'name':'data_test', 
   'type':'const', 
   'value':'42;', 
   'export':None, 
   'default':None, 
   'start_regex':''}),
 (
  "export let data_test2 = {\n    key: 'value',\n};",
  {'name':'data_test2', 
   'type':'let', 
   'value':"{\n    key: 'value',\n};", 
   'export':'export ', 
   'default':None, 
   'start_regex':''}),
 (
  'var dataTest3 = [\n    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\n];',
  {'name':'dataTest3', 
   'type':'var', 
   'value':'[\n    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\n];', 
   'export':None, 
   'default':None, 
   'start_regex':''}),
 ("'const attribute = 42'", None),
 ('const data_test = 42', None)],
  ids=[
 'valid data',
 'valid object data',
 'valid list data',
 'invalid data string',
 'invalid data with no semi-colons'])
def test_data_pattern(content, expected):
    """Match an variable."""
    match = champollion.parser.js_data._DATA_PATTERN.search(content)
    if expected is None:
        @py_assert2 = None
        @py_assert1 = match is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (match, @py_assert2)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
    else:
        @py_assert1 = match.groupdict
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 == expected
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.groupdict\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None