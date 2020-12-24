# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_tokenization.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 13860 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pytest import raises, fixture
from math import exp, log
from concrete import TokenizationKind, TokenLattice, LatticePath, Token, TokenTagging, TaggedToken, Tokenization, Arc, AnnotationMetadata
from concrete.util import create_comm
from concrete.util import get_tokens, get_ner, get_pos, get_lemmas, get_tagged_tokens, compute_lattice_expected_counts, get_token_taggings
import mock

def allclose(x, y, rel_tol=1e-06, abs_tol=1e-09):
    return len(x) == len(y) and len(x) == sum(abs(x[i] - y[i]) <= rel_tol * abs(x[i]) + abs_tol for i in range(len(x)))


@fixture
def tokenization(request):
    return Tokenization(tokenTaggingList=[
     TokenTagging(metadata=AnnotationMetadata(tool='x'), taggingType='?', taggedTokenList=[
      TaggedToken(tokenIndex=0, tag='?'),
      TaggedToken(tokenIndex=1, tag='?'),
      TaggedToken(tokenIndex=2, tag='?')]),
     TokenTagging(metadata=AnnotationMetadata(tool='x'), taggingType='POS', taggedTokenList=[
      TaggedToken(tokenIndex=0, tag='N'),
      TaggedToken(tokenIndex=1, tag='N'),
      TaggedToken(tokenIndex=2, tag='X')]),
     TokenTagging(metadata=AnnotationMetadata(tool='y'), taggingType='NUMERAL', taggedTokenList=[
      TaggedToken(tokenIndex=0, tag='N'),
      TaggedToken(tokenIndex=1, tag='N'),
      TaggedToken(tokenIndex=2, tag='Y')]),
     TokenTagging(metadata=AnnotationMetadata(tool='y'), taggingType='LEMMA', taggedTokenList=[
      TaggedToken(tokenIndex=0, tag='mambo'),
      TaggedToken(tokenIndex=1, tag='number'),
      TaggedToken(tokenIndex=2, tag='4')])])


def test_get_tokens_invalid_kind():
    with raises(ValueError):
        get_tokens(Tokenization(kind='invalid-kind'))


@mock.patch('concrete.util.tokenization.get_tagged_tokens')
def test_get_pos(mock_get_tagged_tokens):
    tokenization = mock.sentinel
    tool = mock.sentinel
    get_pos(tokenization, tool=tool)
    mock_get_tagged_tokens.assert_called_with(tokenization, 'POS', tool=tool)


@mock.patch('concrete.util.tokenization.get_tagged_tokens')
def test_get_lemmas(mock_get_tagged_tokens):
    tokenization = mock.sentinel
    tool = mock.sentinel
    get_lemmas(tokenization, tool=tool)
    mock_get_tagged_tokens.assert_called_with(tokenization, 'LEMMA', tool=tool)


@mock.patch('concrete.util.tokenization.get_tagged_tokens')
def test_get_ner(mock_get_tagged_tokens):
    tokenization = mock.sentinel
    tool = mock.sentinel
    get_ner(tokenization, tool=tool)
    mock_get_tagged_tokens.assert_called_with(tokenization, 'NER', tool=tool)


def test_get_tagged_tokens(tokenization):
    @py_assert0 = [
     'N', 'N', 'Y']
    @py_assert5 = lambda t: t.tag
    @py_assert9 = 'NUMERAL'
    @py_assert11 = get_tagged_tokens(tokenization, @py_assert9)
    @py_assert13 = map(@py_assert5, @py_assert11)
    @py_assert15 = list(@py_assert13)
    @py_assert2 = @py_assert0 == @py_assert15
    if not @py_assert2:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py16)s\n{%(py16)s = %(py3)s(%(py14)s\n{%(py14)s = %(py4)s(%(py6)s, %(py12)s\n{%(py12)s = %(py7)s(%(py8)s, %(py10)s)\n})\n})\n}',), (@py_assert0, @py_assert15)) % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(get_tagged_tokens) if 'get_tagged_tokens' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_tagged_tokens) else 'get_tagged_tokens', 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert0 = [
     0, 1, 2]
    @py_assert5 = lambda t: t.tokenIndex
    @py_assert9 = 'NUMERAL'
    @py_assert11 = get_tagged_tokens(tokenization, @py_assert9)
    @py_assert13 = map(@py_assert5, @py_assert11)
    @py_assert15 = list(@py_assert13)
    @py_assert2 = @py_assert0 == @py_assert15
    if not @py_assert2:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py16)s\n{%(py16)s = %(py3)s(%(py14)s\n{%(py14)s = %(py4)s(%(py6)s, %(py12)s\n{%(py12)s = %(py7)s(%(py8)s, %(py10)s)\n})\n})\n}',), (@py_assert0, @py_assert15)) % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(get_tagged_tokens) if 'get_tagged_tokens' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_tagged_tokens) else 'get_tagged_tokens', 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_get_tagged_tokens_lowercase(tokenization):
    @py_assert0 = [
     'N', 'N', 'Y']
    @py_assert5 = lambda t: t.tag
    @py_assert9 = 'numeral'
    @py_assert11 = get_tagged_tokens(tokenization, @py_assert9)
    @py_assert13 = map(@py_assert5, @py_assert11)
    @py_assert15 = list(@py_assert13)
    @py_assert2 = @py_assert0 == @py_assert15
    if not @py_assert2:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py16)s\n{%(py16)s = %(py3)s(%(py14)s\n{%(py14)s = %(py4)s(%(py6)s, %(py12)s\n{%(py12)s = %(py7)s(%(py8)s, %(py10)s)\n})\n})\n}',), (@py_assert0, @py_assert15)) % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(get_tagged_tokens) if 'get_tagged_tokens' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_tagged_tokens) else 'get_tagged_tokens', 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert0 = [
     0, 1, 2]
    @py_assert5 = lambda t: t.tokenIndex
    @py_assert9 = 'numeral'
    @py_assert11 = get_tagged_tokens(tokenization, @py_assert9)
    @py_assert13 = map(@py_assert5, @py_assert11)
    @py_assert15 = list(@py_assert13)
    @py_assert2 = @py_assert0 == @py_assert15
    if not @py_assert2:
        @py_format17 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py16)s\n{%(py16)s = %(py3)s(%(py14)s\n{%(py14)s = %(py4)s(%(py6)s, %(py12)s\n{%(py12)s = %(py7)s(%(py8)s, %(py10)s)\n})\n})\n}',), (@py_assert0, @py_assert15)) % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py14': @pytest_ar._saferepr(@py_assert13), 'py7': @pytest_ar._saferepr(get_tagged_tokens) if 'get_tagged_tokens' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_tagged_tokens) else 'get_tagged_tokens', 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format19 = ('' + 'assert %(py18)s') % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = None


def test_get_tagged_tokens_no_tagging(tokenization):
    tokenization.tokenTaggingList = filter(lambda ttl: ttl.taggingType != 'NUMERAL', tokenization.tokenTaggingList)
    with raises(Exception):
        get_tagged_tokens(tokenization, 'NUMERAL')


def test_get_tagged_tokens_non_unique_tagging(tokenization):
    tokenization.tokenTaggingList.append(TokenTagging(taggingType='NUMERAL', taggedTokenList=[
     TaggedToken(tokenIndex=0, tag='N'),
     TaggedToken(tokenIndex=1, tag='Y'),
     TaggedToken(tokenIndex=2, tag='Y')]))
    with raises(Exception):
        get_tagged_tokens(tokenization, 'NUMERAL')


def test_get_tagged_tokens_non_unique_tagging_specify_tool(tokenization):
    tokenization.tokenTaggingList.append(TokenTagging(metadata=AnnotationMetadata(tool='z'), taggingType='NUMERAL', taggedTokenList=[
     TaggedToken(tokenIndex=0, tag='N'),
     TaggedToken(tokenIndex=1, tag='Y'),
     TaggedToken(tokenIndex=2, tag='Y')]))
    @py_assert0 = [
     'N', 'N', 'Y']
    @py_assert5 = lambda t: t.tag
    @py_assert9 = 'NUMERAL'
    @py_assert11 = 'y'
    @py_assert13 = get_tagged_tokens(tokenization, @py_assert9, tool=@py_assert11)
    @py_assert15 = map(@py_assert5, @py_assert13)
    @py_assert17 = list(@py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py3)s(%(py16)s\n{%(py16)s = %(py4)s(%(py6)s, %(py14)s\n{%(py14)s = %(py7)s(%(py8)s, %(py10)s, tool=%(py12)s)\n})\n})\n}',), (@py_assert0, @py_assert17)) % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py14': @pytest_ar._saferepr(@py_assert13), 'py18': @pytest_ar._saferepr(@py_assert17), 'py7': @pytest_ar._saferepr(get_tagged_tokens) if 'get_tagged_tokens' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_tagged_tokens) else 'get_tagged_tokens', 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert0 = [
     0, 1, 2]
    @py_assert5 = lambda t: t.tokenIndex
    @py_assert9 = 'NUMERAL'
    @py_assert11 = 'y'
    @py_assert13 = get_tagged_tokens(tokenization, @py_assert9, tool=@py_assert11)
    @py_assert15 = map(@py_assert5, @py_assert13)
    @py_assert17 = list(@py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py3)s(%(py16)s\n{%(py16)s = %(py4)s(%(py6)s, %(py14)s\n{%(py14)s = %(py7)s(%(py8)s, %(py10)s, tool=%(py12)s)\n})\n})\n}',), (@py_assert0, @py_assert17)) % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py14': @pytest_ar._saferepr(@py_assert13), 'py18': @pytest_ar._saferepr(@py_assert17), 'py7': @pytest_ar._saferepr(get_tagged_tokens) if 'get_tagged_tokens' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_tagged_tokens) else 'get_tagged_tokens', 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_get_tagged_tokens_non_unique_tagging_specify_tool_uppercase(tokenization):
    tokenization.tokenTaggingList.append(TokenTagging(metadata=AnnotationMetadata(tool='Z'), taggingType='NUMERAL', taggedTokenList=[
     TaggedToken(tokenIndex=0, tag='N'),
     TaggedToken(tokenIndex=1, tag='Y'),
     TaggedToken(tokenIndex=2, tag='Y')]))
    @py_assert0 = [
     'N', 'N', 'Y']
    @py_assert5 = lambda t: t.tag
    @py_assert9 = 'NUMERAL'
    @py_assert11 = 'y'
    @py_assert13 = get_tagged_tokens(tokenization, @py_assert9, tool=@py_assert11)
    @py_assert15 = map(@py_assert5, @py_assert13)
    @py_assert17 = list(@py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py3)s(%(py16)s\n{%(py16)s = %(py4)s(%(py6)s, %(py14)s\n{%(py14)s = %(py7)s(%(py8)s, %(py10)s, tool=%(py12)s)\n})\n})\n}',), (@py_assert0, @py_assert17)) % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py14': @pytest_ar._saferepr(@py_assert13), 'py18': @pytest_ar._saferepr(@py_assert17), 'py7': @pytest_ar._saferepr(get_tagged_tokens) if 'get_tagged_tokens' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_tagged_tokens) else 'get_tagged_tokens', 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    @py_assert0 = [
     0, 1, 2]
    @py_assert5 = lambda t: t.tokenIndex
    @py_assert9 = 'NUMERAL'
    @py_assert11 = 'y'
    @py_assert13 = get_tagged_tokens(tokenization, @py_assert9, tool=@py_assert11)
    @py_assert15 = map(@py_assert5, @py_assert13)
    @py_assert17 = list(@py_assert15)
    @py_assert2 = @py_assert0 == @py_assert17
    if not @py_assert2:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py18)s\n{%(py18)s = %(py3)s(%(py16)s\n{%(py16)s = %(py4)s(%(py6)s, %(py14)s\n{%(py14)s = %(py7)s(%(py8)s, %(py10)s, tool=%(py12)s)\n})\n})\n}',), (@py_assert0, @py_assert17)) % {'py3': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py12': @pytest_ar._saferepr(@py_assert11), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py14': @pytest_ar._saferepr(@py_assert13), 'py18': @pytest_ar._saferepr(@py_assert17), 'py7': @pytest_ar._saferepr(get_tagged_tokens) if 'get_tagged_tokens' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_tagged_tokens) else 'get_tagged_tokens', 'py1': @pytest_ar._saferepr(@py_assert0), 'py16': @pytest_ar._saferepr(@py_assert15), 'py4': @pytest_ar._saferepr(map) if 'map' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(map) else 'map', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None


def test_get_tagged_tokens_no_tagging_specify_tool(tokenization):
    with raises(Exception):
        get_tagged_tokens(tokenization, 'NUMERAL', tool='z')


def test_get_token_taggings(tokenization):
    @py_assert0 = [
     [
      (0, 'N'), (1, 'N'), (2, 'Y')]]
    @py_assert3 = [[(t.tokenIndex, t.tag) for t in tt.taggedTokenList] for tt in get_token_taggings(tokenization, 'NUMERAL')]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_get_token_taggings_lowercase(tokenization):
    @py_assert0 = [
     [
      (0, 'N'), (1, 'N'), (2, 'Y')]]
    @py_assert3 = [[(t.tokenIndex, t.tag) for t in tt.taggedTokenList] for tt in get_token_taggings(tokenization, 'numeral')]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_get_token_taggings_lowercase_case_sensitive(tokenization):
    @py_assert0 = []
    @py_assert5 = 'numeral'
    @py_assert7 = True
    @py_assert9 = get_token_taggings(tokenization, @py_assert5, case_sensitive=@py_assert7)
    @py_assert2 = @py_assert0 == @py_assert9
    if not @py_assert2:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py10)s\n{%(py10)s = %(py3)s(%(py4)s, %(py6)s, case_sensitive=%(py8)s)\n}', ), (@py_assert0, @py_assert9)) % {'py3': @pytest_ar._saferepr(get_token_taggings) if 'get_token_taggings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_token_taggings) else 'get_token_taggings', 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_get_token_taggings_no_tagging(tokenization):
    @py_assert0 = []
    @py_assert5 = '!NUMERAL'
    @py_assert7 = get_token_taggings(tokenization, @py_assert5)
    @py_assert2 = @py_assert0 == @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py4)s, %(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py3': @pytest_ar._saferepr(get_token_taggings) if 'get_token_taggings' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_token_taggings) else 'get_token_taggings', 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None


def test_get_token_taggings_non_unique_tagging(tokenization):
    tokenization.tokenTaggingList.append(TokenTagging(taggingType='NUMERAL', taggedTokenList=[
     TaggedToken(tokenIndex=0, tag='N'),
     TaggedToken(tokenIndex=1, tag='Y'),
     TaggedToken(tokenIndex=2, tag='Y')]))
    @py_assert0 = [
     [
      (0, 'N'), (1, 'N'), (2, 'Y')], [(0, 'N'), (1, 'Y'), (2, 'Y')]]
    @py_assert3 = [[(t.tokenIndex, t.tag) for t in tt.taggedTokenList] for tt in get_token_taggings(tokenization, 'NUMERAL')]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_no_lattice():
    comm = create_comm('comm-1', 'mambo no. 4')
    tokenization = comm.sectionList[0].sentenceList[0].tokenization
    tokenization.kind = None
    token_texts = [t.text for t in get_tokens(tokenization)]
    @py_assert0 = ['mambo', 'no.', '4']
    @py_assert2 = @py_assert0 == token_texts
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, token_texts)) % {'py3': @pytest_ar._saferepr(token_texts) if 'token_texts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(token_texts) else 'token_texts', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_no_lattice_with_no_kind():
    comm = create_comm('comm-1', 'mambo no. 4')
    tokenization = comm.sectionList[0].sentenceList[0].tokenization
    token_texts = [t.text for t in get_tokens(tokenization)]
    @py_assert0 = ['mambo', 'no.', '4']
    @py_assert2 = @py_assert0 == token_texts
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, token_texts)) % {'py3': @pytest_ar._saferepr(token_texts) if 'token_texts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(token_texts) else 'token_texts', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_lattice_with_token_list_kind():
    comm = create_comm('comm-1', 'mambo no. 4')
    tokenization = comm.sectionList[0].sentenceList[0].tokenization
    lattice_path = LatticePath()
    lattice_path.tokenList = [Token(tokenIndex=0, text='mambo'),
     Token(tokenIndex=0, text='no.'),
     Token(tokenIndex=0, text='3')]
    token_lattice = TokenLattice()
    token_lattice.cachedBestPath = lattice_path
    tokenization.lattice = token_lattice
    token_texts = [t.text for t in get_tokens(tokenization)]
    @py_assert0 = ['mambo', 'no.', '4']
    @py_assert2 = @py_assert0 == token_texts
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, token_texts)) % {'py3': @pytest_ar._saferepr(token_texts) if 'token_texts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(token_texts) else 'token_texts', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_lattice_with_token_lattice_kind():
    comm = create_comm('comm-1', 'mambo no. 4')
    tokenization = comm.sectionList[0].sentenceList[0].tokenization
    lattice_path = LatticePath()
    lattice_path.tokenList = [Token(tokenIndex=0, text='mambo'),
     Token(tokenIndex=0, text='no.'),
     Token(tokenIndex=0, text='3')]
    token_lattice = TokenLattice()
    token_lattice.cachedBestPath = lattice_path
    tokenization.lattice = token_lattice
    tokenization.kind = TokenizationKind.TOKEN_LATTICE
    token_texts = [t.text for t in get_tokens(tokenization)]
    @py_assert0 = ['mambo', 'no.', '3']
    @py_assert2 = @py_assert0 == token_texts
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, token_texts)) % {'py3': @pytest_ar._saferepr(token_texts) if 'token_texts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(token_texts) else 'token_texts', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_lattice_with_no_kind():
    comm = create_comm('comm-1', 'mambo no. 4')
    tokenization = comm.sectionList[0].sentenceList[0].tokenization
    lattice_path = LatticePath()
    lattice_path.tokenList = [Token(tokenIndex=0, text='mambo'),
     Token(tokenIndex=0, text='no.'),
     Token(tokenIndex=0, text='3')]
    token_lattice = TokenLattice()
    token_lattice.cachedBestPath = lattice_path
    tokenization.lattice = token_lattice
    tokenization.kind = None
    token_texts = [t.text for t in get_tokens(tokenization)]
    @py_assert0 = ['mambo', 'no.', '4']
    @py_assert2 = @py_assert0 == token_texts
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, token_texts)) % {'py3': @pytest_ar._saferepr(token_texts) if 'token_texts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(token_texts) else 'token_texts', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_compute_lattice_expected_counts_empty():
    @py_assert2 = []
    @py_assert4 = 0
    @py_assert6 = 0
    @py_assert8 = TokenLattice(arcList=@py_assert2, startState=@py_assert4, endState=@py_assert6)
    @py_assert10 = compute_lattice_expected_counts(@py_assert8)
    @py_assert13 = []
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py0)s(%(py9)s\n{%(py9)s = %(py1)s(arcList=%(py3)s, startState=%(py5)s, endState=%(py7)s)\n})\n} == %(py14)s', ), (@py_assert10, @py_assert13)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py14': @pytest_ar._saferepr(@py_assert13), 'py0': @pytest_ar._saferepr(compute_lattice_expected_counts) if 'compute_lattice_expected_counts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compute_lattice_expected_counts) else 'compute_lattice_expected_counts', 'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(TokenLattice) if 'TokenLattice' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TokenLattice) else 'TokenLattice', 'py11': @pytest_ar._saferepr(@py_assert10), 'py5': @pytest_ar._saferepr(@py_assert4), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_compute_lattice_expected_counts_one_arc():
    expected = [
     0.0]
    actual = compute_lattice_expected_counts(TokenLattice(arcList=[
     Arc(src=0, dst=1, token=Token(tokenIndex=0), weight=-1.0)], startState=0, endState=1))
    @py_assert3 = allclose(expected, actual)
    if not @py_assert3:
        @py_format5 = (@pytest_ar._format_assertmsg('%s !~= %s' % (expected, actual)) + '\n>assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py1': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected', 'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(allclose) if 'allclose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(allclose) else 'allclose'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None


def test_compute_lattice_expected_counts_two_parallel_arcs():
    expected = [
     0.0]
    actual = compute_lattice_expected_counts(TokenLattice(arcList=[
     Arc(src=0, dst=1, token=Token(tokenIndex=0), weight=-1.0),
     Arc(src=0, dst=1, token=Token(tokenIndex=0), weight=-3.0)], startState=0, endState=1))
    @py_assert3 = allclose(expected, actual)
    if not @py_assert3:
        @py_format5 = (@pytest_ar._format_assertmsg('%s !~= %s' % (expected, actual)) + '\n>assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py1': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected', 'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(allclose) if 'allclose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(allclose) else 'allclose'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None


def test_compute_lattice_expected_counts_two_serial_arcs():
    expected = [
     0.0, 0.0]
    actual = compute_lattice_expected_counts(TokenLattice(arcList=[
     Arc(src=0, dst=1, token=Token(tokenIndex=0), weight=-1.0),
     Arc(src=1, dst=2, token=Token(tokenIndex=1), weight=-3.0)], startState=0, endState=2))
    @py_assert3 = allclose(expected, actual)
    if not @py_assert3:
        @py_format5 = (@pytest_ar._format_assertmsg('%s !~= %s' % (expected, actual)) + '\n>assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py1': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected', 'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(allclose) if 'allclose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(allclose) else 'allclose'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None


def test_compute_lattice_expected_counts_triangle():
    A = log(exp(-3) + exp(-4))
    expected = [-3 - A, 0.0]
    actual = compute_lattice_expected_counts(TokenLattice(arcList=[
     Arc(src=0, dst=1, token=Token(tokenIndex=0), weight=-1.0),
     Arc(src=1, dst=2, token=Token(tokenIndex=1), weight=-2.0),
     Arc(src=0, dst=2, token=Token(tokenIndex=1), weight=-4.0)], startState=0, endState=2))
    @py_assert3 = allclose(expected, actual)
    if not @py_assert3:
        @py_format5 = (@pytest_ar._format_assertmsg('%s !~= %s' % (expected, actual)) + '\n>assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py1': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected', 'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(allclose) if 'allclose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(allclose) else 'allclose'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None


def test_compute_lattice_expected_counts_triangle_arbitrary_states():
    A = log(exp(-3) + exp(-4))
    expected = [-3 - A, 0.0]
    actual = compute_lattice_expected_counts(TokenLattice(arcList=[
     Arc(src=47, dst=9, token=Token(tokenIndex=0), weight=-1.0),
     Arc(src=9, dst=3, token=Token(tokenIndex=1), weight=-2.0),
     Arc(src=47, dst=3, token=Token(tokenIndex=1), weight=-4.0)], startState=47, endState=3))
    @py_assert3 = allclose(expected, actual)
    if not @py_assert3:
        @py_format5 = (@pytest_ar._format_assertmsg('%s !~= %s' % (expected, actual)) + '\n>assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py1': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected', 'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(allclose) if 'allclose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(allclose) else 'allclose'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None


def test_compute_lattice_expected_counts_rhombus():
    A = log(exp(-3) + exp(-7))
    expected = [0.0, -3 - A, -7 - A]
    actual = compute_lattice_expected_counts(TokenLattice(arcList=[
     Arc(src=0, dst=1, token=Token(tokenIndex=0), weight=-1.0),
     Arc(src=1, dst=3, token=Token(tokenIndex=1), weight=-2.0),
     Arc(src=0, dst=2, token=Token(tokenIndex=0), weight=-3.0),
     Arc(src=2, dst=3, token=Token(tokenIndex=2), weight=-4.0)], startState=0, endState=3))
    @py_assert3 = allclose(expected, actual)
    if not @py_assert3:
        @py_format5 = (@pytest_ar._format_assertmsg('%s !~= %s' % (expected, actual)) + '\n>assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py1': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected', 'py2': @pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(allclose) if 'allclose' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(allclose) else 'allclose'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None


def test_compute_lattice_expected_counts_incomplete_arc():
    with raises(ValueError):
        compute_lattice_expected_counts(TokenLattice(arcList=[
         Arc(dst=1, token=Token(tokenIndex=0), weight=-1.0)], startState=0, endState=1))
    with raises(ValueError):
        compute_lattice_expected_counts(TokenLattice(arcList=[
         Arc(src=0, token=Token(tokenIndex=0), weight=-1.0)], startState=0, endState=1))
    with raises(ValueError):
        compute_lattice_expected_counts(TokenLattice(arcList=[
         Arc(src=0, dst=1, weight=-1.0)], startState=0, endState=1))
    with raises(ValueError):
        compute_lattice_expected_counts(TokenLattice(arcList=[
         Arc(src=0, dst=1, token=Token(tokenIndex=0))], startState=0, endState=1))