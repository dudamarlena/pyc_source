# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_validate_communication.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 6753 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, time
from testfixtures import LogCapture, StringComparison
import concrete
from concrete.util import add_references_to_communication
from concrete.validate import validate_communication, validate_entity_mention_ids, validate_entity_mention_tokenization_ids, validate_token_offsets_for_section, validate_thrift_deep, validate_token_offsets_for_sentence
from concrete import Section, Sentence, TextSpan, Token, TokenList, Tokenization
from test_helper import read_test_comm

def create_section_with_sentence(section_start, section_ending, sentence_start, sentence_ending):
    sentence_textspan = TextSpan(start=sentence_start, ending=sentence_ending)
    sentence = Sentence(textSpan=sentence_textspan, uuid='TEST_SENTENCE')
    section_textspan = TextSpan(start=section_start, ending=section_ending)
    section = Section(sentenceList=[
     sentence], textSpan=section_textspan, uuid='TEST_SECTION')
    return section


def create_sentence_with_token(sentence_start, sentence_ending, token_start, token_ending):
    token_textspan = TextSpan(start=token_start, ending=token_ending)
    token = Token(textSpan=token_textspan)
    tokenization = Tokenization(tokenList=TokenList(tokenList=[token]))
    sentence_textspan = TextSpan(start=sentence_start, ending=sentence_ending)
    sentence = Sentence(tokenization=tokenization, textSpan=sentence_textspan, uuid='TEST')
    return sentence


def test_add_references():
    comm = read_test_comm()
    add_references_to_communication(comm)


def test_entity_mention_ids():
    comm = read_test_comm()
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert2 = validate_entity_mention_ids(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_entity_mention_ids) if 'validate_entity_mention_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_entity_mention_ids) else 'validate_entity_mention_ids'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    comm.entitySetList[0].entityList[0].mentionIdList[0] = concrete.UUID(uuidString='BAD_ENTITY_MENTION_UUID')
    with LogCapture() as (log_capture):
        @py_assert2 = validate_entity_mention_ids(comm)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_entity_mention_ids) if 'validate_entity_mention_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_entity_mention_ids) else 'validate_entity_mention_ids'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None
    log_capture.check(('root', 'ERROR',
     StringComparison('.*invalid entityMentionId.*BAD_ENTITY_MENTION_UUID')))


def test_entity_mention_tokenization():
    comm = read_test_comm()
    @py_assert2 = validate_communication(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    @py_assert2 = validate_entity_mention_ids(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_entity_mention_ids) if 'validate_entity_mention_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_entity_mention_ids) else 'validate_entity_mention_ids'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None
    comm.entityMentionSetList[0].mentionList[0].tokens.tokenizationId = concrete.UUID(uuidString='BAD_TOKENIZATION_UUID')
    with LogCapture() as (log_capture):
        @py_assert2 = validate_entity_mention_tokenization_ids(comm)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_entity_mention_tokenization_ids) if 'validate_entity_mention_tokenization_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_entity_mention_tokenization_ids) else 'validate_entity_mention_tokenization_ids'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None
    log_capture.check(('root', 'ERROR',
     StringComparison('.*invalid tokenizationId.*BAD_TOKENIZATION_UUID')))


def test_check_required_fields():
    comm = concrete.Communication()
    with LogCapture() as (log_capture):
        @py_assert2 = validate_thrift_deep(comm)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_thrift_deep) if 'validate_thrift_deep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_thrift_deep) else 'validate_thrift_deep'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None
    log_capture.check(('root', 'ERROR', "Communication: Required Field 'id' is unset!"))
    comm.id = 'ID'
    with LogCapture() as (log_capture):
        @py_assert2 = validate_thrift_deep(comm)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_thrift_deep) if 'validate_thrift_deep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_thrift_deep) else 'validate_thrift_deep'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None
    log_capture.check(('root', 'ERROR', "Communication: Required Field 'uuid' is unset!"))
    comm.uuid = concrete.UUID(uuidString='TEST_UUID')
    with LogCapture() as (log_capture):
        @py_assert2 = validate_thrift_deep(comm)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_thrift_deep) if 'validate_thrift_deep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_thrift_deep) else 'validate_thrift_deep'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None
    log_capture.check(('root', 'ERROR',
     StringComparison(".*TEST_UUID.*Required Field 'type' is unset!")))
    comm.metadata = concrete.AnnotationMetadata(tool='TEST', timestamp=int(time.time()))
    comm.type = 'OTHER'
    @py_assert2 = validate_thrift_deep(comm)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py0': @pytest_ar._saferepr(validate_thrift_deep) if 'validate_thrift_deep' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_thrift_deep) else 'validate_thrift_deep'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None


def test_validate_token_offsets_for_good_sentence():
    sentence = create_sentence_with_token(0, 30, 0, 10)
    @py_assert2 = validate_token_offsets_for_sentence(sentence)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(sentence) if 'sentence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentence) else 'sentence', 'py0': @pytest_ar._saferepr(validate_token_offsets_for_sentence) if 'validate_token_offsets_for_sentence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_token_offsets_for_sentence) else 'validate_token_offsets_for_sentence'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None


def test_validate_token_offsets_for_sentence_rev_sentence_offsets():
    sentence = create_sentence_with_token(30, 0, 0, 10)
    with LogCapture():
        @py_assert2 = validate_token_offsets_for_sentence(sentence)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(sentence) if 'sentence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentence) else 'sentence', 'py0': @pytest_ar._saferepr(validate_token_offsets_for_sentence) if 'validate_token_offsets_for_sentence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_token_offsets_for_sentence) else 'validate_token_offsets_for_sentence'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None


def test_validate_token_offsets_for_sentence_rev_token_offsets():
    sentence = create_sentence_with_token(0, 30, 10, 0)
    with LogCapture():
        @py_assert2 = validate_token_offsets_for_sentence(sentence)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(sentence) if 'sentence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentence) else 'sentence', 'py0': @pytest_ar._saferepr(validate_token_offsets_for_sentence) if 'validate_token_offsets_for_sentence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_token_offsets_for_sentence) else 'validate_token_offsets_for_sentence'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None


def test_validate_token_offsets_for_sentence_token_outside():
    sentence = create_sentence_with_token(0, 30, 25, 35)
    with LogCapture():
        @py_assert2 = validate_token_offsets_for_sentence(sentence)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(sentence) if 'sentence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sentence) else 'sentence', 'py0': @pytest_ar._saferepr(validate_token_offsets_for_sentence) if 'validate_token_offsets_for_sentence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_token_offsets_for_sentence) else 'validate_token_offsets_for_sentence'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None


def test_validate_token_offsets_for_good_section():
    section = create_section_with_sentence(0, 30, 0, 10)
    @py_assert2 = validate_token_offsets_for_section(section)
    if not @py_assert2:
        @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(section) if 'section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(section) else 'section', 'py0': @pytest_ar._saferepr(validate_token_offsets_for_section) if 'validate_token_offsets_for_section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_token_offsets_for_section) else 'validate_token_offsets_for_section'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert2 = None


def test_validate_token_offsets_for_section_rev_section_offsets():
    section = create_section_with_sentence(30, 0, 0, 10)
    with LogCapture():
        @py_assert2 = validate_token_offsets_for_section(section)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(section) if 'section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(section) else 'section', 'py0': @pytest_ar._saferepr(validate_token_offsets_for_section) if 'validate_token_offsets_for_section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_token_offsets_for_section) else 'validate_token_offsets_for_section'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None


def test_validate_token_offsets_for_section_rev_token_offsets():
    section = create_section_with_sentence(0, 30, 10, 0)
    with LogCapture():
        @py_assert2 = validate_token_offsets_for_section(section)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(section) if 'section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(section) else 'section', 'py0': @pytest_ar._saferepr(validate_token_offsets_for_section) if 'validate_token_offsets_for_section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_token_offsets_for_section) else 'validate_token_offsets_for_section'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None


def test_validate_token_offsets_for_section_sentence_outside():
    section = create_section_with_sentence(0, 30, 25, 35)
    with LogCapture():
        @py_assert2 = validate_token_offsets_for_section(section)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(section) if 'section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(section) else 'section', 'py0': @pytest_ar._saferepr(validate_token_offsets_for_section) if 'validate_token_offsets_for_section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_token_offsets_for_section) else 'validate_token_offsets_for_section'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None


def test_validate_token_offsets_for_real_example_section_data():
    section = create_section_with_sentence(55, 296, 0, 118)
    with LogCapture():
        @py_assert2 = validate_token_offsets_for_section(section)
        @py_assert4 = not @py_assert2
        if not @py_assert4:
            @py_format5 = ('' + 'assert not %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(section) if 'section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(section) else 'section', 'py0': @pytest_ar._saferepr(validate_token_offsets_for_section) if 'validate_token_offsets_for_section' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_token_offsets_for_section) else 'validate_token_offsets_for_section'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert2 = @py_assert4 = None