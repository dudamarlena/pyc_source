# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_inspect.py
# Compiled at: 2018-09-14 12:30:07
# Size of source mod 2**32: 18338 bytes
from __future__ import unicode_literals
from __future__ import print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, re
from pytest import mark
from mock import Mock, sentinel
from concrete.inspect import _get_conll_tags_for_tokenization, print_situation_mentions, print_conll_style_tags_for_communication
from concrete.util import generate_UUID, create_comm
from concrete.util.references import add_references_to_communication
from concrete.util.tokenization import get_tokenizations, get_tokens
from concrete import AnnotationMetadata, Communication, Dependency, DependencyParse, EntityMention, EntityMentionSet, MentionArgument, Property, Section, Sentence, SituationMention, SituationMentionSet, TextSpan, TokenRefSequence, Tokenization, TokenizationKind, Token, TokenList, TokenTagging, TaggedToken

def _comm_with_properties(num_properties):
    ts = 17
    meta_tokn = AnnotationMetadata(tool='tokn-tool', timestamp=ts)
    toks = TokenList(tokenList=[
     Token(tokenIndex=0, text='text', textSpan=TextSpan(start=0, ending=1))])
    tokn = Tokenization(uuid=generate_UUID(), metadata=meta_tokn, kind=TokenizationKind.TOKEN_LIST, tokenList=toks)
    sentence = Sentence(uuid=generate_UUID(), tokenization=tokn)
    section = Section(uuid=generate_UUID(), kind='kind', label='label', sentenceList=[
     sentence])
    trfs = TokenRefSequence(tokenizationId=tokn.uuid, tokenIndexList=[
     0], anchorTokenIndex=0)
    em = EntityMention(uuid=generate_UUID(), entityType='entityType', text='text', tokens=trfs)
    meta_ems = AnnotationMetadata(tool='ems-tool', timestamp=ts)
    ems = EntityMentionSet(uuid=generate_UUID(), metadata=meta_ems, mentionList=[
     em])
    meta_prop = AnnotationMetadata(tool='Annotator1', timestamp=ts)
    props = list(Property(value='Property%d' % i, metadata=meta_prop, polarity=4.0) for i in range(num_properties))
    am = MentionArgument(role='role', entityMentionId=em.uuid, propertyList=props)
    sm = SituationMention(uuid=generate_UUID(), tokens=trfs, argumentList=[am])
    meta_sms = AnnotationMetadata(tool='sms-tool', timestamp=ts)
    sms = SituationMentionSet(uuid=generate_UUID(), metadata=meta_sms, mentionList=[
     sm])
    meta_comm = AnnotationMetadata(tool='tool', timestamp=ts)
    comm = Communication(uuid=generate_UUID(), id='id', text='text', type='type', metadata=meta_comm, sectionList=[
     section], situationMentionSetList=[
     sms], entityMentionSetList=[
     ems])
    add_references_to_communication(comm)
    return comm


def comm_with_other_tags(*additional_tagging_types):
    comm = create_comm('quick', 'The quick brown fox jumped\nover the lazy dog .\n\nOr did she ?\n')
    for section in comm.sectionList:
        for sentence in section.sentenceList:
            sentence.tokenization.tokenTaggingList = [
             TokenTagging(uuid=generate_UUID(), metadata=AnnotationMetadata(tool='tool', timestamp=1), taggingType='upper', taggedTokenList=[TaggedToken(tokenIndex=token.tokenIndex, tag=token.text.upper()) for token in sentence.tokenization.tokenList.tokenList]),
             TokenTagging(uuid=generate_UUID(), metadata=AnnotationMetadata(tool='tool', timestamp=1), taggingType='lower', taggedTokenList=[TaggedToken(tokenIndex=token.tokenIndex, tag=token.text.lower()) for token in sentence.tokenization.tokenList.tokenList])] + [TokenTagging(uuid=generate_UUID(), metadata=AnnotationMetadata(tool='tool/{}'.format(i), timestamp=1), taggingType=tagging_type, taggedTokenList=[TaggedToken(tokenIndex=token.tokenIndex, tag='{}_{}/{}'.format(tagging_type, token.tokenIndex, i)) for token in sentence.tokenization.tokenList.tokenList]) for i, tagging_type in enumerate(additional_tagging_types)]

    return comm


def test_print_conll_char_offsets(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags(), char_offsets=True)


def test_print_conll_missing_tags(capsys):
    comm = create_comm('quick', 'The quick brown fox jumped\nover the lazy dog .\n\nOr did she ?\n')
    print_conll_style_tags_for_communication(comm, ner=True)
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\n-----\t-----\n1\tThe\n2\tquick\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_print_conll_missing_char_offsets(capsys):
    comm_without_token_textspans = comm_with_other_tags()
    for tokenization in get_tokenizations(comm_without_token_textspans):
        for token in get_tokens(tokenization):
            token.textSpan = None

    print_conll_style_tags_for_communication(comm_without_token_textspans, char_offsets=True)
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\tCHAR\n-----\t-----\t----\n1\tThe\t\n2\tquick\t\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_print_conll_other_tags_ignore_all(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags())
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\n-----\t-----\n1\tThe\n2\tquick\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_print_conll_other_tags_ignore_some(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags(), other_tags=dict(upper=None))
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\tupper\n-----\t-----\t-----\n1\tThe\tTHE\n2\tquick\tQUICK\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = '3\tshe\tSHE\n'
    @py_assert2 = @py_assert0 in out
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_print_conll_other_tags(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags(), other_tags=dict(upper=None, lower=None))
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = []
    @py_assert3 = []
    @py_assert5 = out.startswith
    @py_assert7 = 'INDEX\tTOKEN\tupper\tlower\n-----\t-----\t-----\t-----\n1\tThe\tTHE\tthe\n2\tquick\tQUICK\tquick\n'
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert2 = @py_assert9
    if @py_assert9:
        @py_assert12 = '3\tshe\tSHE\tshe\n'
        @py_assert14 = @py_assert12 in out
        @py_assert2 = @py_assert14
    @py_assert0 = @py_assert2
    if not @py_assert2:
        @py_assert23 = []
        @py_assert25 = out.startswith
        @py_assert27 = 'INDEX\tTOKEN\tlower\tupper\n-----\t-----\t-----\t-----\n1\tThe\tthe\tTHE\n2\tquick\tquick\tQUICK\n'
        @py_assert29 = @py_assert25(@py_assert27)
        @py_assert22 = @py_assert29
        if @py_assert29:
            @py_assert32 = '3\tshe\tshe\tSHE\n'
            @py_assert34 = @py_assert32 in out
            @py_assert22 = @py_assert34
        @py_assert0 = @py_assert22
    if not @py_assert0:
        @py_format11 = '%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s.startswith\n}(%(py8)s)\n}' % {'py8': @pytest_ar._saferepr(@py_assert7), 'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_assert3.append(@py_format11)
        if @py_assert9:
            @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert14,), ('%(py13)s in %(py15)s', ), (@py_assert12, out)) % {'py15': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py13': @pytest_ar._saferepr(@py_assert12)}
            @py_format18 = '%(py17)s' % {'py17': @py_format16}
            @py_assert3.append(@py_format18)
        @py_format19 = @pytest_ar._format_boolop(@py_assert3, 0) % {}
        @py_format21 = '%(py20)s' % {'py20': @py_format19}
        @py_assert1.append(@py_format21)
        if not @py_assert2:
            @py_format31 = '%(py30)s\n{%(py30)s = %(py26)s\n{%(py26)s = %(py24)s.startswith\n}(%(py28)s)\n}' % {'py30': @pytest_ar._saferepr(@py_assert29), 'py26': @pytest_ar._saferepr(@py_assert25), 'py24': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py28': @pytest_ar._saferepr(@py_assert27)}
            @py_assert23.append(@py_format31)
            if @py_assert29:
                @py_format36 = @pytest_ar._call_reprcompare(('in', ), (@py_assert34,), ('%(py33)s in %(py35)s', ), (@py_assert32, out)) % {'py33': @pytest_ar._saferepr(@py_assert32), 'py35': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out'}
                @py_format38 = '%(py37)s' % {'py37': @py_format36}
                @py_assert23.append(@py_format38)
            @py_format39 = @pytest_ar._format_boolop(@py_assert23, 0) % {}
            @py_format41 = '%(py40)s' % {'py40': @py_format39}
            @py_assert1.append(@py_format41)
        @py_format42 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format44 = 'assert %(py43)s' % {'py43': @py_format42}
        raise AssertionError(@pytest_ar._format_explanation(@py_format44))
    @py_assert0 = @py_assert1 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = @py_assert22 = @py_assert23 = @py_assert25 = @py_assert27 = @py_assert29 = @py_assert32 = @py_assert34 = None


def test_print_conll_other_tags_repeated_other_tag(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags('upper', 'ner'), ner=True, other_tags=dict(upper=None))
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\tNER\tupper\tupper\n-----\t-----\t---\t-----\t-----\n1\tThe\tner_0/1\tTHE\tupper_0/0\n2\tquick\tner_1/1\tQUICK\tupper_1/0\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = '3\tshe\tner_2/1\tSHE\tupper_2/0\n'
    @py_assert2 = @py_assert0 in out
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_print_conll_other_tags_repeated_other_tag_filtered(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags('upper', 'ner'), ner=True, other_tags=dict(upper=lambda anns: filter(lambda ann: ann.metadata.tool == 'tool/0', anns)))
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\tNER\tupper\n-----\t-----\t---\t-----\n1\tThe\tner_0/1\tupper_0/0\n2\tquick\tner_1/1\tupper_1/0\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = '3\tshe\tner_2/1\tupper_2/0\n'
    @py_assert2 = @py_assert0 in out
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_print_conll_other_tags_repeated_ner(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags('ner', 'ner'), ner=True, other_tags=dict(upper=None))
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\tNER\tNER\tupper\n-----\t-----\t---\t---\t-----\n1\tThe\tner_0/0\tner_0/1\tTHE\n2\tquick\tner_1/0\tner_1/1\tQUICK\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = '3\tshe\tner_2/0\tner_2/1\tSHE\n'
    @py_assert2 = @py_assert0 in out
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_print_conll_other_tags_repeated_ner_filtered(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags('ner', 'ner'), ner=True, other_tags=dict(upper=None), ner_filter=lambda anns: filter(lambda ann: ann.metadata.tool == 'tool/1', anns))
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\tNER\tupper\n-----\t-----\t---\t-----\n1\tThe\tner_0/1\tTHE\n2\tquick\tner_1/1\tQUICK\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = '3\tshe\tner_2/1\tSHE\n'
    @py_assert2 = @py_assert0 in out
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_print_conll_start_tags(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags(), starts=True)
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\tSTART\n-----\t-----\t-----\n1\tThe\t0\n2\tquick\t4\n3\tbrown\t10\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_print_conll_ending_tags(capsys):
    print_conll_style_tags_for_communication(comm_with_other_tags(), endings=True)
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = out.startswith
    @py_assert3 = 'INDEX\tTOKEN\tENDING\n-----\t-----\t------\n1\tThe\t3\n2\tquick\t9\n3\tbrown\t15\n'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py4)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_print_situation_mentions(capsys):
    comm = _comm_with_properties(0)
    print_situation_mentions(comm)
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = re.search
    @py_assert3 = 'SituationMention\\s+(\\d+)-(\\d+):\\n'
    @py_assert6 = @py_assert1(@py_assert3, out)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = re.search
    @py_assert3 = 'situationType:'
    @py_assert6 = @py_assert1(@py_assert3, out)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = re.search
    @py_assert3 = 'situationKind:'
    @py_assert6 = @py_assert1(@py_assert3, out)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = re.search
    @py_assert3 = 'intensity:'
    @py_assert6 = @py_assert1(@py_assert3, out)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None


def test_print_situation_mentions_with_type(capsys):
    comm = _comm_with_properties(0)
    comm.situationMentionSetList[0].mentionList[0].situationType = 'st'
    print_situation_mentions(comm)
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = re.search
    @py_assert3 = 'SituationMention +(\\d+)-(\\d+):\\n +situationType: +st\\n'
    @py_assert6 = @py_assert1(@py_assert3, out)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = re.search
    @py_assert3 = 'situationKind:'
    @py_assert6 = @py_assert1(@py_assert3, out)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = re.search
    @py_assert3 = 'intensity:'
    @py_assert6 = @py_assert1(@py_assert3, out)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None


def test_print_situation_mentions_with_kind(capsys):
    comm = _comm_with_properties(0)
    comm.situationMentionSetList[0].mentionList[0].situationKind = 'sk'
    print_situation_mentions(comm)
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = re.search
    @py_assert3 = 'SituationMention +(\\d+)-(\\d+):\\n +situationKind: +sk\\n'
    @py_assert6 = @py_assert1(@py_assert3, out)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = re.search
    @py_assert3 = 'situationType:'
    @py_assert6 = @py_assert1(@py_assert3, out)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = re.search
    @py_assert3 = 'intensity:'
    @py_assert6 = @py_assert1(@py_assert3, out)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None


def test_print_situation_mentions_with_intensity(capsys):
    comm = _comm_with_properties(0)
    comm.situationMentionSetList[0].mentionList[0].intensity = 3.5
    print_situation_mentions(comm)
    out, err = capsys.readouterr()
    @py_assert2 = ''
    @py_assert1 = err == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = re.search
    @py_assert3 = 'SituationMention +(\\d+)-(\\d+):\\n +intensity: +3\\.50*\\n'
    @py_assert6 = @py_assert1(@py_assert3, out)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = re.search
    @py_assert3 = 'situationType:'
    @py_assert6 = @py_assert1(@py_assert3, out)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = re.search
    @py_assert3 = 'situationKind:'
    @py_assert6 = @py_assert1(@py_assert3, out)
    @py_assert8 = not @py_assert6
    if not @py_assert8:
        @py_format9 = ('' + 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py4)s, %(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6), 'py5': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None


def test_print_situation_mentions_without_properties(capsys):
    print_situation_mentions(_comm_with_properties(0))
    out, err = capsys.readouterr()
    @py_assert0 = 'Properties'
    @py_assert2 = @py_assert0 not in out
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, out)) % {'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


@mark.parametrize('num_properties', [(1, ), (2, ), (3, )])
def test_print_situation_mentions_with_properties(capsys, num_properties):
    num_properties = 3
    print_situation_mentions(_comm_with_properties(num_properties))
    out, err = capsys.readouterr()
    @py_assert0 = 1
    @py_assert4 = out.count
    @py_assert6 = 'Properties'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert2 = @py_assert0 == @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.count\n}(%(py7)s)\n}', ), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert0 = 1
    @py_assert4 = out.count
    @py_assert6 = 'Annotator1'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert2 = @py_assert0 == @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.count\n}(%(py7)s)\n}', ), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert3 = out.count
    @py_assert5 = 'Property'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert1 = num_properties == @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.count\n}(%(py6)s)\n}', ), (num_properties, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(num_properties) if 'num_properties' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_properties) else 'num_properties', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert3 = out.count
    @py_assert5 = '4.0'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert1 = num_properties == @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.count\n}(%(py6)s)\n}', ), (num_properties, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(num_properties) if 'num_properties' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_properties) else 'num_properties', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_get_conll_tags_no_token_list():
    tokenization = Tokenization()
    @py_assert2 = _get_conll_tags_for_tokenization(tokenization)
    @py_assert5 = []
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    mock_filter = Mock(return_value=[])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter) if 'mock_filter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter) else 'mock_filter', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None


def test_get_conll_tags_zero_tokens_implicit_filter():
    tokenization = Tokenization(tokenList=TokenList(tokenList=[]), dependencyParseList=[
     DependencyParse(dependencyList=[])])
    @py_assert2 = _get_conll_tags_for_tokenization(tokenization)
    @py_assert5 = [[]]
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_get_conll_tags_zero_tokens():
    tokenization = Tokenization(tokenList=TokenList(tokenList=[]), dependencyParseList=sentinel.dpl)
    mock_filter = Mock(return_value=[
     DependencyParse(dependencyList=[])])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter)
    @py_assert6 = [[]]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter) if 'mock_filter' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter) else 'mock_filter', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter.assert_called_with(sentinel.dpl)


def test_get_conll_tags_one_token_implicit_filter():
    tokenization = Tokenization(tokenList=TokenList(tokenList=[
     Token(tokenIndex=0, text='t0')]), dependencyParseList=[
     DependencyParse(dependencyList=[
      Dependency(gov=-1, dep=0, edgeType='edge_0/0')])])
    @py_assert2 = _get_conll_tags_for_tokenization(tokenization)
    @py_assert5 = [[('0', 'edge_0/0')]]
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_get_conll_tags_one_token():
    tokenization = Tokenization(tokenList=TokenList(tokenList=[
     Token(tokenIndex=0, text='t0')]), dependencyParseList=sentinel.dpl)
    mock_filter_zero = Mock(return_value=[])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter_zero)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter_zero) if 'mock_filter_zero' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter_zero) else 'mock_filter_zero', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter_zero.assert_called_with(sentinel.dpl)
    mock_filter_one_empty = Mock(return_value=[
     DependencyParse(dependencyList=[])])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter_one_empty)
    @py_assert6 = [[('', '')]]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter_one_empty) if 'mock_filter_one_empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter_one_empty) else 'mock_filter_one_empty', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter_one_empty.assert_called_with(sentinel.dpl)
    mock_filter_one = Mock(return_value=[
     DependencyParse(dependencyList=[
      Dependency(gov=-1, dep=0, edgeType='edge_0/0')])])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter_one)
    @py_assert6 = [[('0', 'edge_0/0')]]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter_one) if 'mock_filter_one' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter_one) else 'mock_filter_one', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter_one.assert_called_with(sentinel.dpl)
    mock_filter_two = Mock(return_value=[
     DependencyParse(dependencyList=[
      Dependency(gov=-1, dep=0, edgeType='edge_0/0')]),
     DependencyParse(dependencyList=[
      Dependency(gov=-1, dep=0, edgeType='edge_0/1')])])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter_two)
    @py_assert6 = [[('0', 'edge_0/0')], [('0', 'edge_0/1')]]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter_two) if 'mock_filter_two' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter_two) else 'mock_filter_two', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter_two.assert_called_with(sentinel.dpl)


def test_get_conll_tags_two_tokens():
    tokenization = Tokenization(tokenList=TokenList(tokenList=[
     Token(tokenIndex=0, text='t0'),
     Token(tokenIndex=1, text='t1')]), dependencyParseList=sentinel.dpl)
    mock_filter_zero = Mock(return_value=[])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter_zero)
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter_zero) if 'mock_filter_zero' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter_zero) else 'mock_filter_zero', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter_zero.assert_called_with(sentinel.dpl)
    mock_filter_one_empty = Mock(return_value=[
     DependencyParse(dependencyList=[])])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter_one_empty)
    @py_assert6 = [[('', ''), ('', '')]]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter_one_empty) if 'mock_filter_one_empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter_one_empty) else 'mock_filter_one_empty', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter_one_empty.assert_called_with(sentinel.dpl)
    mock_filter_one_half_empty = Mock(return_value=[
     DependencyParse(dependencyList=[
      Dependency(gov=0, dep=1, edgeType='edge_1/0')])])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter_one_half_empty)
    @py_assert6 = [[('', ''), ('1', 'edge_1/0')]]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter_one_half_empty) if 'mock_filter_one_half_empty' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter_one_half_empty) else 'mock_filter_one_half_empty', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter_one_half_empty.assert_called_with(sentinel.dpl)
    mock_filter_one = Mock(return_value=[
     DependencyParse(dependencyList=[
      Dependency(gov=-1, dep=0, edgeType='edge_0/0'),
      Dependency(gov=0, dep=1, edgeType='edge_1/0')])])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter_one)
    @py_assert6 = [[('0', 'edge_0/0'), ('1', 'edge_1/0')]]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter_one) if 'mock_filter_one' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter_one) else 'mock_filter_one', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter_one.assert_called_with(sentinel.dpl)
    mock_filter_two = Mock(return_value=[
     DependencyParse(dependencyList=[
      Dependency(gov=-1, dep=0, edgeType='edge_0/0'),
      Dependency(gov=0, dep=1, edgeType='edge_1/0')]),
     DependencyParse(dependencyList=[
      Dependency(gov=-1, dep=0, edgeType='edge_0/1'),
      Dependency(gov=0, dep=1, edgeType='edge_1/1')])])
    @py_assert3 = _get_conll_tags_for_tokenization(tokenization, mock_filter_two)
    @py_assert6 = [[('0', 'edge_0/0'), ('1', 'edge_1/0')], [('0', 'edge_0/1'), ('1', 'edge_1/1')]]
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(tokenization) if 'tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tokenization) else 'tokenization', 'py2': @pytest_ar._saferepr(mock_filter_two) if 'mock_filter_two' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_filter_two) else 'mock_filter_two', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(_get_conll_tags_for_tokenization) if '_get_conll_tags_for_tokenization' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_get_conll_tags_for_tokenization) else '_get_conll_tags_for_tokenization'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert3 = @py_assert5 = @py_assert6 = None
    mock_filter_two.assert_called_with(sentinel.dpl)