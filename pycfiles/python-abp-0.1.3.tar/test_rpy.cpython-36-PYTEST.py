# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_rpy.py
# Compiled at: 2019-06-05 11:48:03
# Size of source mod 2**32: 4451 bytes
"""Functional tests for testing rPython integration."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from collections import namedtuple
import pytest
from abp.filters.rpy import line2dict, lines2dicts
_SAMPLE_TUPLE = namedtuple('tuple', 'foo,bar')
_TEST_EXAMPLES = {'header':{'in':'[Adblock Plus 2.0]', 
  'out':{'type':'Header', 
   'version':'Adblock Plus 2.0'}}, 
 'metadata':{'in':'! Title: Example list', 
  'out':{'type':'Metadata', 
   'key':'Title', 
   'value':'Example list'}}, 
 'comment':{'in':'! Comment', 
  'out':{'type':'Comment', 
   'text':'Comment'}}, 
 'empty':{'in':'', 
  'out':{'type': 'EmptyLine'}}, 
 'include':{'in':'%include www.test.py/filtelist.txt%', 
  'out':{'type':'Include', 
   'target':'www.test.py/filtelist.txt'}}, 
 'filter_single':{'in':'foo.com##div#ad1', 
  'out':{'type':'Filter', 
   'text':'foo.com##div#ad1', 
   'selector':{'type':'css', 
    'value':'div#ad1'}, 
   'action':'hide', 
   'options':{'domain': {'foo.com': True}}}}, 
 'filter_with_%':{'in':'%22banner%*%22idzone%', 
  'out':{'type':'Filter', 
   'text':'%22banner%*%22idzone%', 
   'selector':{'type':'url-pattern', 
    'value':'%22banner%*%22idzone%'}, 
   'action':'block', 
   'options':{}}}, 
 'filter_multiple':{'in':'foo.com,bar.com##div#ad1', 
  'out':{'type':'Filter', 
   'text':'foo.com,bar.com##div#ad1', 
   'selector':{'type':'css', 
    'value':'div#ad1'}, 
   'action':'hide', 
   'options':{'domain': {'foo.com':True,  'bar.com':True}}}}, 
 'filter_with_sitekey_list':{'in':'@@bla$ping,domain=foo.com|~bar.foo.com,sitekey=foo|bar', 
  'out':{'text':'@@bla$ping,domain=foo.com|~bar.foo.com,sitekey=foo|bar', 
   'selector':{'value':'bla', 
    'type':'url-pattern'}, 
   'action':'allow', 
   'options':{'ping':True, 
    'domain':{'foo.com':True, 
     'bar.foo.com':False}, 
    'sitekey':[
     'foo', 'bar']}, 
   'type':'Filter'}}}

@pytest.mark.parametrize('line_type', list(_TEST_EXAMPLES.keys()))
def test_line2dict_format(line_type):
    """Test that the API result has the appropriate format.

    Checks for both keys and datatypes.
    """
    position = 'start' if line_type in frozenset({'header', 'metadata'}) else 'body'
    data = line2dict(_TEST_EXAMPLES[line_type]['in'], position)
    @py_assert2 = _TEST_EXAMPLES[line_type]['out']
    @py_assert1 = data == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_rpy.py', lineno=120)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (data, @py_assert2)) % {'py0':@pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_lines2dicts_start_mode():
    """Test that the API returns the correct result in the appropriate format.

    Checks for 'start' mode, which can handle headers and metadata.
    """
    tests = [t for t in _TEST_EXAMPLES.values()]
    ins = [ex['in'] for ex in tests]
    outs = [ex['out'] for ex in tests]
    @py_assert2 = 'start'
    @py_assert4 = lines2dicts(ins, @py_assert2)
    @py_assert6 = @py_assert4 == outs
    if @py_assert6 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_rpy.py', lineno=132)
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py7)s', ), (@py_assert4, outs)) % {'py0':@pytest_ar._saferepr(lines2dicts) if 'lines2dicts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines2dicts) else 'lines2dicts',  'py1':@pytest_ar._saferepr(ins) if 'ins' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ins) else 'ins',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(outs) if 'outs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(outs) else 'outs'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None


def test_lines2dicts_default():
    """Test that the API returns the correct result in the appropriate format.

    By default, lines2dicts() does not correctly parse headers and metadata.
    """
    tests = [t for t in _TEST_EXAMPLES.values() if t['out']['type'] not in frozenset({'Metadata', 'Header'})]
    ins = [ex['in'] for ex in tests]
    outs = [ex['out'] for ex in tests]
    @py_assert2 = lines2dicts(ins)
    @py_assert4 = @py_assert2 == outs
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_rpy.py', lineno=145)
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, outs)) % {'py0':@pytest_ar._saferepr(lines2dicts) if 'lines2dicts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lines2dicts) else 'lines2dicts',  'py1':@pytest_ar._saferepr(ins) if 'ins' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ins) else 'ins',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(outs) if 'outs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(outs) else 'outs'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None