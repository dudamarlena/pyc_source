# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/parser/test_parser_helper.py
# Compiled at: 2017-07-03 15:20:46
# Size of source mod 2**32: 10056 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, os, champollion.parser.helper

@pytest.mark.parametrize(('content_lines', 'line_number', 'expected'),
  [
 (
  [
   '/**',
   ' * An function example.',
   ' *',
   ' * Detailed description.',
   ' *',
   ' * .. note::',
   ' *',
   ' *     A note.',
   ' */',
   'function sum(a, b) {',
   '    return a+b;',
   '}'],
  10,
  'An function example.\n\nDetailed description.\n\n.. note::\n\n    A note.'),
 (
  [
   '/** A cool data. */',
   'const Data = null'],
  2,
  'A cool data.'),
 (
  [
   '/*',
   ' * Incorrect docstring',
   ' */',
   'function doSomething() {',
   "    console.log('something');",
   '}'],
  4,
  None),
 (
  [
   '/*',
   '',
   ' Incorrect docstring',
   '',
   '*/',
   'function doSomethingElse() {',
   "    console.log('something_else');",
   '}'],
  6,
  None),
 (
  [
   '// Incorrect docstring',
   'function doSomethingElse() {',
   "    console.log('something_else');",
   '}'],
  2,
  None),
 (
  [
   '',
   'function doSomethingElse() {',
   "    console.log('something_else');",
   '}'],
  2,
  None),
 (
  [
   '/** A cool data. */',
   'const Data = null'],
  1,
  None)],
  ids=[
 'valid element line number with multiline docstring',
 'valid element line number with one line docstring',
 'valid element line number with incorrect docstring 1',
 'valid element line number with incorrect docstring 2',
 'valid element line number with incorrect docstring 3',
 'valid element line number with no docstring',
 'invalid line_number'])
def test_get_docstrings(content_lines, line_number, expected):
    """Return docstrings from a element's line number."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.helper
    @py_assert5 = @py_assert3.get_docstring
    @py_assert9 = @py_assert5(line_number, content_lines)
    @py_assert11 = @py_assert9 == expected
    if not @py_assert11:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.helper\n}.get_docstring\n}(%(py7)s, %(py8)s)\n} == %(py12)s', ), (@py_assert9, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(line_number) if 'line_number' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(line_number) else 'line_number',  'py8':@pytest_ar._saferepr(content_lines) if 'content_lines' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content_lines) else 'content_lines',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert9 = @py_assert11 = None


def test_filter_comments():
    """Remove all comments from content"""
    content = "'use strict'; /* a beautiful comment */\n\n/*\na long comment that can take a lot of places so\nwe put it on several lines.\n*/\n\n// a data docstring\nconst DATA = 1;\n\n/**\n * Function docstring\n */\nfunction sum(a, b) {\n    // Return the sum of a and b\n    return a+b;\n}\n\nconst url = 'http://somewhere.com';\n\n"
    expected = "'use strict'; \n\n\n\n\n\n\n\nconst DATA = 1;\n\n\n\n\nfunction sum(a, b) {\n    \n    return a+b;\n}\n\nconst url = 'http://somewhere.com';\n\n"
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.helper
    @py_assert5 = @py_assert3.filter_comments
    @py_assert8 = @py_assert5(content)
    @py_assert10 = @py_assert8 == expected
    if not @py_assert10:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.helper\n}.filter_comments\n}(%(py7)s)\n} == %(py11)s', ), (@py_assert8, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None


def test_filter_comments_keep_content_size():
    """Remove all comments from content while keeping content size."""
    content = "'use strict'; /* a beautiful comment */\n\n/*\na long comment that can take a lot of places so\nwe put it on several lines.\n*/\n\n// a data docstring\nconst DATA = 1;\n\n/**\n * Function docstring\n */\nfunction sum(a, b) {\n    // Return the sum of a and b\n    return a+b;\n}\n\nconst url = 'http://somewhere.com';\n\n"
    expected = "'use strict'; {comment1}\n\n{comment2}\n\n\n\n\n{comment3}\nconst DATA = 1;\n\n{comment4}\n\n\nfunction sum(a, b) {{\n    {comment5}\n    return a+b;\n}}\n\nconst url = 'http://somewhere.com';\n\n".format(comment1=(' ' * len('/* a beautiful comment */')),
      comment2=(' ' * len('/*a long comment that can take a lot of places sowe put it on several lines.*/')),
      comment3=(' ' * len('// a data docstring')),
      comment4=(' ' * len('/** * Function docstring */')),
      comment5=(' ' * len('// Return the sum of a and b')))
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.helper
    @py_assert5 = @py_assert3.filter_comments
    @py_assert8 = True
    @py_assert10 = @py_assert5(content, keep_content_size=@py_assert8)
    @py_assert12 = @py_assert10 == expected
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.helper\n}.filter_comments\n}(%(py7)s, keep_content_size=%(py9)s)\n} == %(py13)s', ), (@py_assert10, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None


def test_filter_comments_without_multiline_comments():
    """Remove all comments from content without multiline comments."""
    content = "'use strict'; /* a beautiful comment */\n\n/*\na long comment that can take a lot of places so\nwe put it on several lines.\n*/\n\n// a data docstring\nconst DATA = 1;\n\n/**\n * Function docstring\n */\nfunction sum(a, b) {\n    // Return the sum of a and b\n    return a+b;\n}\n\nconst url = 'http://somewhere.com';\n\n"
    expected = "'use strict'; /* a beautiful comment */\n\n/*\na long comment that can take a lot of places so\nwe put it on several lines.\n*/\n\n\nconst DATA = 1;\n\n/**\n * Function docstring\n */\nfunction sum(a, b) {\n    \n    return a+b;\n}\n\nconst url = 'http://somewhere.com';\n\n"
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.helper
    @py_assert5 = @py_assert3.filter_comments
    @py_assert8 = False
    @py_assert10 = @py_assert5(content, filter_multiline_comment=@py_assert8)
    @py_assert12 = @py_assert10 == expected
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.helper\n}.filter_comments\n}(%(py7)s, filter_multiline_comment=%(py9)s)\n} == %(py13)s', ), (@py_assert10, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None


@pytest.mark.parametrize(('content', 'expected_content', 'expected_collapsed_content'),
  [
 (
  'const emptyObject = {};',
  'const emptyObject = {};', {}),
 (
  'let test = {a: 1, b: 2, c: 3};',
  'let test = {};',
  {1: '{a: 1, b: 2, c: 3}'}),
 (
  'const element = {\n    key1: value1,\n    key2: value2,\n    key3: value3,\n};\n\nfunction sum(a, b) {\n    return a+b\n}\n\n',
  'const element = {}\n\n\n\n;\n\nfunction sum(a, b) {}\n\n\n\n',
  {1:'{\n    key1: value1,\n    key2: value2,\n    key3: value3,\n}', 
   7:'{\n    return a+b\n}'}),
 (
  'class AwesomeClass {\n    constructor() {\n        this.data = 1;\n    }\n\n    increase() {\n        this.data += 1;\n    }\n}\n',
  'class AwesomeClass {}\n\n\n\n\n\n\n\n\n',
  {1:'{\n    constructor() {\n        this.data = 1;\n    }\n\n    increase() {\n        this.data += 1;\n    }\n}', 
   2:'{\n        this.data = 1;\n    }', 
   6:'{\n        this.data += 1;\n    }'})],
  ids=[
 'empty object',
 'simple object',
 'objects and functions on multiple lines',
 'nested class'])
def test_collapse_all(content, expected_content, expected_collapsed_content):
    """Collapse all objects, classes and functions."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.helper
    @py_assert5 = @py_assert3.collapse_all
    @py_assert8 = @py_assert5(content)
    @py_assert11 = (
     expected_content, expected_collapsed_content)
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.helper\n}.collapse_all\n}(%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert11 = None