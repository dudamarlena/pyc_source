# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/tests/unit/test_ruleset.py
# Compiled at: 2018-08-17 09:32:41
# Size of source mod 2**32: 3643 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest
from colin.core.exceptions import ColinRulesetException
from colin.core.ruleset.ruleset import Ruleset

def test_ruleset_yaml():
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    lol_ruleset_path = os.path.join(tests_dir, 'data', 'lol-ruleset.yaml')
    with open(lol_ruleset_path, 'r') as (fd):
        r = Ruleset(ruleset_file=fd)
        checks = r.get_checks(None)
    @py_assert2 = len(checks)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_ruleset_json():
    tests_dir = os.path.dirname(os.path.dirname(__file__))
    lol_ruleset_path = os.path.join(tests_dir, 'data', 'lol-ruleset.json')
    with open(lol_ruleset_path, 'r') as (fd):
        r = Ruleset(ruleset_file=fd)
        checks = r.get_checks(None)
    @py_assert2 = len(checks)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_ruleset_tags():
    tags = [
     'a', 'banana']
    r = {'version':'1', 
     'checks':[
      {'name':'name_label', 
       'tags':tags[:]}]}
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None)
    @py_assert2 = len(checks)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = checks[0]
    @py_assert2 = @py_assert0.tags
    @py_assert4 = @py_assert2 == tags
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.tags\n} == %(py5)s', ), (@py_assert2, tags)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(tags) if 'tags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tags) else 'tags'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_ruleset_additional_tags():
    tags = [
     'a']
    r = {'version':'1', 
     'checks':[
      {'name':'name_label', 
       'additional_tags':tags[:]}]}
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None)
    @py_assert2 = len(checks)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert3 = set(tags)
    @py_assert5 = @py_assert3.intersection
    @py_assert8 = checks[0]
    @py_assert10 = @py_assert8.tags
    @py_assert12 = set(@py_assert10)
    @py_assert14 = @py_assert5(@py_assert12)
    @py_assert16 = list(@py_assert14)
    @py_assert18 = @py_assert16 == tags
    if not @py_assert18:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert18,), ('%(py17)s\n{%(py17)s = %(py0)s(%(py15)s\n{%(py15)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py1)s(%(py2)s)\n}.intersection\n}(%(py13)s\n{%(py13)s = %(py7)s(%(py11)s\n{%(py11)s = %(py9)s.tags\n})\n})\n})\n} == %(py19)s',), (@py_assert16, tags)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py2':@pytest_ar._saferepr(tags) if 'tags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tags) else 'tags',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py19':@pytest_ar._saferepr(tags) if 'tags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tags) else 'tags'}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None


@pytest.mark.parametrize('tags,expected_check_name', [
 (
  [
   'banana'], None),
 (
  [
   'name'], 'name_label')])
def test_ruleset_tags_filtering(tags, expected_check_name):
    r = {'version':'1', 
     'checks':[
      {'name': 'name_label'}]}
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None, tags=tags)
    if expected_check_name:
        @py_assert2 = len(checks)
        @py_assert5 = 1
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = checks[0]
        @py_assert2 = @py_assert0.name
        @py_assert4 = @py_assert2 == expected_check_name
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py5)s', ), (@py_assert2, expected_check_name)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(expected_check_name) if 'expected_check_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_check_name) else 'expected_check_name'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
    else:
        @py_assert2 = len(checks)
        @py_assert5 = 0
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None


@pytest.mark.parametrize('version,should_raise', [
 (1, False),
 ('1', False),
 ('banana', True),
 (None, True),
 ('', True),
 ('<blank>', True)])
def test_ruleset_version(version, should_raise):
    if version == '<blank>':
        r = {'banana': 123}
    else:
        r = {'version': version}
    if should_raise:
        with pytest.raises(ColinRulesetException):
            Ruleset(ruleset=r)
    else:
        @py_assert2 = Ruleset(ruleset=r)
        if not @py_assert2:
            @py_format4 = 'assert %(py3)s\n{%(py3)s = %(py0)s(ruleset=%(py1)s)\n}' % {'py0':@pytest_ar._saferepr(Ruleset) if 'Ruleset' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Ruleset) else 'Ruleset',  'py1':@pytest_ar._saferepr(r) if 'r' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(r) else 'r',  'py3':@pytest_ar._saferepr(@py_assert2)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format4))
        @py_assert2 = None


def test_ruleset_override():
    m = 'my-message!'
    r = {'version':'1', 
     'checks':[
      {'name':'name_label', 
       'tags':[
        'a', 'b'], 
       'just':'testing', 
       'message':m}]}
    r = Ruleset(ruleset=r)
    checks = r.get_checks(None)
    @py_assert2 = len(checks)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = checks[0]
    @py_assert2 = @py_assert0.message
    @py_assert4 = @py_assert2 == m
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.message\n} == %(py5)s', ), (@py_assert2, m)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(m) if 'm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(m) else 'm'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = checks[0]
    @py_assert2 = @py_assert0.just
    @py_assert5 = 'testing'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.just\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None