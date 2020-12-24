# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py
# Compiled at: 2019-06-13 06:59:11
# Size of source mod 2**32: 8461 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from abp.filters import parse_line, parse_filterlist, ParseError, SelectorType as SelType, FilterAction, FilterOption
from abp.filters.parser import Comment, Metadata, Header

def test_parse_empty():
    line = parse_line('    ')
    @py_assert1 = line.type
    @py_assert4 = 'emptyline'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=29)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(line) if 'line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(line) else 'line'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@pytest.mark.parametrize('filter_text, expected', {'*asdf*d**dd*': {'selector': {'type': SelType.URL_PATTERN, 'value': '*asdf*d**dd*'}, 
                  'action': FilterAction.BLOCK}, 
 
 '@@|*asd|f*d**dd*|': {'selector': {'type': SelType.URL_PATTERN, 'value': '|*asd|f*d**dd*|'}, 
                       'action': FilterAction.ALLOW}, 
 
 '/ddd|f?a[s]d/': {'selector': {'type': SelType.URL_REGEXP, 'value': 'ddd|f?a[s]d'}, 
                   'action': FilterAction.BLOCK}, 
 
 '@@/ddd|f?a[s]d/': {'selector': {'type': SelType.URL_REGEXP, 'value': 'ddd|f?a[s]d'}, 
                     'action': FilterAction.ALLOW}, 
 
 'bla$match-case,~script,domain=foo.com|~bar.com,sitekey=foo': {'selector': {'type': SelType.URL_PATTERN, 'value': 'bla'}, 
                                                                'action': FilterAction.BLOCK, 
                                                                'options': [
                                                                            (
                                                                             FilterOption.MATCH_CASE, True),
                                                                            (
                                                                             FilterOption.SCRIPT, False),
                                                                            (
                                                                             FilterOption.DOMAIN, [('foo.com', True), ('bar.com', False)]),
                                                                            (
                                                                             FilterOption.SITEKEY, ['foo'])]}, 
 
 '@@http://bla$~script,~other,sitekey=foo|bar': {'selector': {'type': SelType.URL_PATTERN, 'value': 'http://bla'}, 
                                                 'action': FilterAction.ALLOW, 
                                                 'options': [
                                                             (
                                                              FilterOption.SCRIPT, False),
                                                             (
                                                              FilterOption.OTHER, False),
                                                             (
                                                              FilterOption.SITEKEY, ['foo', 'bar'])]}, 
 
 "||foo.com^$csp=script-src 'self' * 'unsafe-inline',script,sitekey=foo," + 'other,match-case,domain=foo.com': {'selector': {'type': SelType.URL_PATTERN, 'value': '||foo.com^'}, 
                                                                                                                'action': FilterAction.BLOCK, 
                                                                                                                'options': [
                                                                                                                            (
                                                                                                                             FilterOption.CSP, "script-src 'self' * 'unsafe-inline'"),
                                                                                                                            ('script', True),
                                                                                                                            (
                                                                                                                             'sitekey', ['foo']),
                                                                                                                            ('other', True),
                                                                                                                            ('match-case', True),
                                                                                                                            (
                                                                                                                             'domain', [('foo.com', True)])]}, 
 
 '@@bla$script,other,domain=foo.com|~bar.foo.com,csp=c s p': {'selector': {'type': SelType.URL_PATTERN, 'value': 'bla'}, 
                                                              'action': FilterAction.ALLOW, 
                                                              'options': [
                                                                          ('script', True),
                                                                          ('other', True),
                                                                          (
                                                                           'domain', [('foo.com', True), ('bar.foo.com', False)]),
                                                                          ('csp', 'c s p')]}, 
 
 '||content.server.com/files/*.php$rewrite=$1': {'selector': {'type': SelType.URL_PATTERN, 
                                                              'value': '||content.server.com/files/*.php'}, 
                                                 
                                                 'action': FilterAction.BLOCK, 
                                                 'options': [
                                                             ('rewrite', '$1')]}, 
 
 '##ddd': {'selector': {'type': SelType.CSS, 'value': 'ddd'}, 
           'action': FilterAction.HIDE, 
           'options': []}, 
 
 '#@#body > div:first-child': {'selector': {'type': SelType.CSS, 'value': 'body > div:first-child'}, 
                               'action': FilterAction.SHOW, 
                               'options': []}, 
 
 'foo,~bar##ddd': {'options': [(FilterOption.DOMAIN, [('foo', True), ('bar', False)])]}, 
 
 'foo,~bar#?#:-abp-properties(abc)': {'selector': {'type': SelType.XCSS, 'value': ':-abp-properties(abc)'}, 
                                      'action': FilterAction.HIDE, 
                                      'options': [(FilterOption.DOMAIN, [('foo', True), ('bar', False)])]}, 
 
 'foo.com#?#aaa :-abp-properties(abc) bbb': {'selector': {'type': SelType.XCSS, 
                                                          'value': 'aaa :-abp-properties(abc) bbb'}}, 
 
 '#?#:-abp-properties(|background-image: url(data:*))': {'selector': {'type': SelType.XCSS, 
                                                                      'value': ':-abp-properties(|background-image: url(data:*))'}, 
                                                         
                                                         'options': []}, 
 
 'foo,~bar#$#abort-on-property-write aaa; abort-on-property-read bbb': {'selector': {'type': SelType.SNIPPET, 
                                                                                     'value': 'abort-on-property-write aaa; abort-on-property-read bbb'}, 
                                                                        
                                                                        'action': FilterAction.HIDE, 
                                                                        'options': [(FilterOption.DOMAIN, [('foo', True), ('bar', False)])]}}.items())
def test_parse_filters(filter_text, expected):
    """Parametric test for filter parsing."""
    parsed = parse_line(filter_text)
    @py_assert1 = parsed.type
    @py_assert4 = 'filter'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=147)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(parsed) if 'parsed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parsed) else 'parsed'}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = parsed.text
    @py_assert3 = @py_assert1 == filter_text
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=148)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py4)s',), (@py_assert1, filter_text)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(filter_text) if 'filter_text' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filter_text) else 'filter_text', 'py0': @pytest_ar._saferepr(parsed) if 'parsed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parsed) else 'parsed'}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    for attribute, expected_value in expected.items():
        @py_assert3 = getattr(parsed, attribute)
        @py_assert5 = @py_assert3 == expected_value
        if @py_assert5 is None:
            from _pytest.warning_types import PytestAssertRewriteWarning
            from warnings import warn_explicit
            warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=150)
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py6)s',), (@py_assert3, expected_value)) % {'py2': @pytest_ar._saferepr(attribute) if 'attribute' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(attribute) else 'attribute', 'py6': @pytest_ar._saferepr(expected_value) if 'expected_value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_value) else 'expected_value', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(getattr) if 'getattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(getattr) else 'getattr', 'py1': @pytest_ar._saferepr(parsed) if 'parsed' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parsed) else 'parsed'}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert3 = @py_assert5 = None


def test_parse_comment():
    line = parse_line('! Block foo')
    @py_assert1 = line.type
    @py_assert4 = 'comment'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=155)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(line) if 'line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(line) else 'line'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = line.text
    @py_assert4 = 'Block foo'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=156)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(line) if 'line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(line) else 'line'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_parse_instruction():
    line = parse_line('%include foo:bar/baz.txt%')
    @py_assert1 = line.type
    @py_assert4 = 'include'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=161)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(line) if 'line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(line) else 'line'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = line.target
    @py_assert4 = 'foo:bar/baz.txt'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=162)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.target\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(line) if 'line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(line) else 'line'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_parse_bad_instruction():
    with pytest.raises(ParseError):
        parse_line('%include%')


def test_parse_start():
    @py_assert1 = '[Adblock Plus 1.1]'
    @py_assert3 = 'start'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'header'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=172)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = 'foo[Adblock Plus 1.1] bar'
    @py_assert3 = 'start'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'header'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=174)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '[Adblock Minus 1.1]'
    @py_assert3 = 'start'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'filter'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=177)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '[Adblock 1.1]'
    @py_assert3 = 'start'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'filter'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=179)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '! Foo: bar'
    @py_assert3 = 'metadata'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'metadata'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=183)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_parse_metadata():
    @py_assert1 = '[Adblock 1.1]'
    @py_assert3 = 'metadata'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'filter'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=188)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '! Foo: bar'
    @py_assert3 = 'metadata'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'metadata'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=190)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_parse_body():
    @py_assert1 = '[Adblock 1.1]'
    @py_assert3 = 'body'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'filter'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=195)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '! Foo: bar'
    @py_assert3 = 'body'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'comment'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=197)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = '! Checksum: 42'
    @py_assert3 = 'body'
    @py_assert5 = parse_line(@py_assert1, @py_assert3)
    @py_assert7 = @py_assert5.type
    @py_assert10 = 'metadata'
    @py_assert9 = @py_assert7 == @py_assert10
    if @py_assert9 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=199)
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n}.type\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(@py_assert3), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(parse_line) if 'parse_line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(parse_line) else 'parse_line', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_parse_invalid_position():
    with pytest.raises(ValueError):
        parse_line('', 'nonsense')


def test_parse_filterlist():
    result = parse_filterlist(['[Adblock Plus 1.1]',
     ' ! Last modified: 26 Jul 2018 02:10 UTC ',
     '! Homepage  :  http://aaa.com/b',
     '||example.com^',
     '! Checksum: OaopkIiiAl77sSHk/VAWDA',
     '! Note: bla bla'])
    @py_assert2 = next(result)
    @py_assert6 = 'Adblock Plus 1.1'
    @py_assert8 = Header(@py_assert6)
    @py_assert4 = @py_assert2 == @py_assert8
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=215)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n}',), (@py_assert2, @py_assert8)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Header) if 'Header' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Header) else 'Header', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert2 = next(result)
    @py_assert6 = 'Last modified'
    @py_assert8 = '26 Jul 2018 02:10 UTC '
    @py_assert10 = Metadata(@py_assert6, @py_assert8)
    @py_assert4 = @py_assert2 == @py_assert10
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=217)
    if not @py_assert4:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py11)s\n{%(py11)s = %(py5)s(%(py7)s, %(py9)s)\n}',), (@py_assert2, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Metadata) if 'Metadata' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Metadata) else 'Metadata', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert2 = next(result)
    @py_assert6 = 'Homepage'
    @py_assert8 = 'http://aaa.com/b'
    @py_assert10 = Metadata(@py_assert6, @py_assert8)
    @py_assert4 = @py_assert2 == @py_assert10
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=218)
    if not @py_assert4:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py11)s\n{%(py11)s = %(py5)s(%(py7)s, %(py9)s)\n}',), (@py_assert2, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Metadata) if 'Metadata' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Metadata) else 'Metadata', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert2 = next(result)
    @py_assert4 = @py_assert2.type
    @py_assert7 = 'filter'
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=219)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}.type\n} == %(py8)s',), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py1': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert2 = next(result)
    @py_assert6 = 'Checksum'
    @py_assert8 = 'OaopkIiiAl77sSHk/VAWDA'
    @py_assert10 = Metadata(@py_assert6, @py_assert8)
    @py_assert4 = @py_assert2 == @py_assert10
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=220)
    if not @py_assert4:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py11)s\n{%(py11)s = %(py5)s(%(py7)s, %(py9)s)\n}',), (@py_assert2, @py_assert10)) % {'py11': @pytest_ar._saferepr(@py_assert10), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Metadata) if 'Metadata' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Metadata) else 'Metadata', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format14 = ('' + 'assert %(py13)s') % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert2 = next(result)
    @py_assert4 = @py_assert2.type
    @py_assert7 = 'comment'
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=221)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}.type\n} == %(py8)s',), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py1': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    with pytest.raises(StopIteration):
        next(result)


def test_exception_timing():
    result = parse_filterlist(['! good line', '%includes bad%'])
    @py_assert2 = next(result)
    @py_assert6 = 'good line'
    @py_assert8 = Comment(@py_assert6)
    @py_assert4 = @py_assert2 == @py_assert8
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=229)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py9)s\n{%(py9)s = %(py5)s(%(py7)s)\n}', ), (@py_assert2, @py_assert8)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(Comment) if 'Comment' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Comment) else 'Comment', 'py0': @pytest_ar._saferepr(next) if 'next' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(next) else 'next', 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    with pytest.raises(ParseError):
        next(result)


def test_parse_line_bytes():
    line = parse_line(b'! \xc3\xbc')
    @py_assert1 = line.text
    @py_assert4 = 'ü'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_parser.py', lineno=236)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(line) if 'line' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(line) else 'line'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None