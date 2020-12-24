# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fnd/Dev/TiddlyWeb/plugins/differ/test/test_differ.py
# Compiled at: 2012-12-14 15:46:36
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, tiddlywebplugins.differ as differ

def test_diff():
    diff = differ.diff
    a = 'lorem ipsum'
    b = 'lorem foo ipsum'
    actual = diff(a, b)
    expected = '- lorem ipsum\n+ lorem foo ipsum\n?       ++++\n'
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    actual = diff(a, b, 'unified')
    expected = '--- \n\n+++ \n\n@@ -1 +1 @@\n\n-lorem ipsum\n+lorem foo ipsum'
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    actual = diff(a, b, 'horizontal')
    expected = '<tr><td class="diff_next" id="difflib_chg_to0__0"><a href="#difflib_chg_to0__top">t</a></td><td class="diff_header" id="from0_1">1</td><td>lorem ipsum</td><td class="diff_next"><a href="#difflib_chg_to0__top">t</a></td><td class="diff_header" id="to0_1">1</td><td>lorem <span class="diff_add">foo </span>ipsum</td></tr>'
    @py_assert1 = expected in actual
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (expected, actual)) % {'py0': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected', 'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    actual = diff(a, b, 'inline')
    expected = 'lorem <ins>foo </ins>ipsum'
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_generate_inline_diff():
    generate_inline_diff = differ.generate_inline_diff
    a = 'lorem ipsum'
    b = 'lorem foo ipsum'
    actual = generate_inline_diff(a, b)
    expected = 'lorem <ins>foo </ins>ipsum'
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    a = 'dolor sit amet'
    b = 'dolor amet'
    actual = generate_inline_diff(a, b)
    expected = 'dolor <del>sit </del>amet'
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    a = 'foo bar baz'
    b = 'foo xxx baz'
    actual = generate_inline_diff(a, b)
    expected = 'foo <del>bar</del><ins>xxx</ins> baz'
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    a = 'foo bar baz\n\nlorem ipsum\ndolor sit amet'
    b = 'foo baz\n\nlorem xxx ipsum\ndolor yyy amet'
    actual = generate_inline_diff(a, b)
    expected = 'foo<del> bar</del> baz <br />\n <br />\nlorem<ins> xxx</ins> ipsum <br />\ndolor <del>sit</del><ins>yyy</ins> amet'
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    a = 'foo bar \nbaz'
    b = 'foo \nbar baz'
    actual = generate_inline_diff(a, b)
    expected = 'foo <ins> <br />\n</ins>bar <del> <br />\n</del>baz'
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    a = '< foo | bar & baz'
    b = 'foo & bar & baz >'
    actual = generate_inline_diff(a, b)
    expected = '<del>&lt; </del>foo <del>|</del><ins>&amp;</ins> bar &amp; baz<ins> &gt;</ins>'
    @py_assert1 = actual == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (actual, expected)) % {'py0': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() is not @py_builtins.globals() else 'actual', 'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() is not @py_builtins.globals() else 'expected'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return