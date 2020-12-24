# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/utils/fortranformat/_parser.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 13918 bytes
from ._lexer import Token
from ._edit_descriptors import *
from ._exceptions import *
from . import config

def parser(tokens, version=None):
    eds = _parse_tokens(tokens, reversion=False, version=None)
    reversion_eds = _parse_tokens(tokens, reversion=True, version=None)
    return (eds, reversion_eds)


def _parse_tokens(tokens, reversion=False, version=None):
    tokens = _remove_outer_parens(tokens)
    if reversion == True:
        tokens = _get_reversion_tokens(tokens)
    tokens = _expand_parens(tokens)
    token_sets = _split_on_commas(tokens)
    token_sets = _split_on_ed9(token_sets)
    token_sets = _split_on_ed10(token_sets)
    token_sets = _split_on_ed8(token_sets)
    eds = []
    for token_set in token_sets:
        ed_type = None
        ed_value = None
        for token in token_set:
            if token.type in ('ED1', 'ED2', 'ED3', 'ED4', 'ED5', 'ED6', 'ED7', 'ED8',
                              'ED9', 'ED10', 'QUOTED_STRING'):
                ed_type = token.type
                ed_value = token.value
                break

        if ed_type is None:
            pass
        else:
            repeat = None
            if ed_value in REPEATABLE_EDS:
                if token_set[0].type in ('NZUINT', 'UINT'):
                    repeat = token_set[0].value
                    token_set = token_set[1:]
            if ed_type == 'QUOTED_STRING':
                ed = _read_quoted_string(token_set)
            else:
                if ed_type == 'ED1':
                    ed = _read_ed1(token_set)
                else:
                    if ed_type == 'ED2':
                        ed = _read_ed2(token_set)
                    else:
                        if ed_type == 'ED3':
                            ed = _read_ed3(token_set)
                        else:
                            if ed_type == 'ED4':
                                ed = _read_ed4(token_set)
                            else:
                                if ed_type == 'ED5':
                                    ed = _read_ed5(token_set)
                                else:
                                    if ed_type == 'ED6':
                                        ed = _read_ed6(token_set)
                                    else:
                                        if ed_type == 'ED7':
                                            ed = _read_ed7(token_set)
                                        else:
                                            if ed_type == 'ED8':
                                                ed = _read_ed8(token_set)
                                            else:
                                                if ed_type == 'ED9':
                                                    ed = _read_ed9(token_set)
                                                else:
                                                    if ed_type == 'ED10':
                                                        ed = _read_ed10(token_set)
                                                    else:
                                                        raise InvalidFormat('Could not identify edit descriptor in sequence $s' % str(token_set))
            if repeat is not None:
                ed.repeat = repeat
            eds.append(ed)

    return eds


def _expand_parens(tokens):
    new_tokens = []
    get_tokens = iter(tokens)
    for t0 in get_tokens:
        if t0.type != 'LEFT_PARENS':
            new_tokens.append(t0)
        else:
            paren_tokens = []
            nesting = 1
            while nesting > 0:
                try:
                    t1 = next(get_tokens)
                except StopIteration:
                    raise InvalidFormat('Open parens in format')

                if t1.type == 'LEFT_PARENS':
                    nesting = nesting + 1
                else:
                    if t1.type == 'RIGHT_PARENS':
                        nesting = nesting - 1
                paren_tokens.append(t1)

            paren_tokens = paren_tokens[:-1]
            if len(new_tokens) > 0 and new_tokens[(-1)].type in ('NZUINT', 'UINT'):
                repeat = new_tokens[(-1)].value
                new_tokens = new_tokens[:-1]
                new_tokens.extend(repeat * (_expand_parens(paren_tokens) + [Token('COMMA', None)]))
            else:
                new_tokens.extend(_expand_parens(paren_tokens))

    return new_tokens


def _split_on_commas(tokens):
    token_sets = []
    set_buff = []
    for t0 in tokens:
        if t0.type == 'COMMA':
            token_sets.append(set_buff)
            set_buff = []
        else:
            set_buff.append(t0)

    token_sets.append(set_buff)
    return token_sets


def _split_on_ed9(token_sets):
    """Splits on :"""
    new_token_sets = []
    for token_set in token_sets:
        if 'ED9' not in [t.type for t in token_set]:
            new_token_sets.append(token_set)
        else:
            buff = []
            for token in token_set:
                if token.type == 'ED9':
                    if len(buff) > 0:
                        new_token_sets.append(buff)
                        buff = []
                    new_token_sets.append([token])
                else:
                    buff.append(token)

            if len(buff) > 0:
                new_token_sets.append([token])

    return new_token_sets


def _split_on_ed10(token_sets):
    """Splits on /"""
    new_token_sets = []
    for token_set in token_sets:
        if len(token_set) > 2:
            if token_set[0].type in ('UINT', 'NZUINT'):
                if token_set[1].type == 'ED10':
                    new_token_sets.append(token_set[:2])
                    token_set = token_set[2:]
            buff = []
            for token in token_set:
                if token.type == 'ED10':
                    if len(buff) > 0:
                        new_token_sets.append(buff)
                        buff = []
                    new_token_sets.append([token])
                else:
                    buff.append(token)

            if len(buff) > 0:
                new_token_sets.append(buff)

    return new_token_sets


def _split_on_ed8(token_sets):
    """Splits on ED8 (i.e. P edit descriptors)"""
    new_token_sets = []
    for token_set in token_sets:
        if 'ED8' not in [t.type for t in token_set]:
            new_token_sets.append(token_set)
        elif token_set[0].type in ('INT', 'UINT', 'NZUINT') and token_set[1].type == 'ED8':
            new_token_sets.append(token_set[:2])
            new_token_sets.append(token_set[2:])
        else:
            raise InvalidFormat('P edit descriptor in invalid position')

    return new_token_sets


def _get_reversion_tokens(tokens):
    reversion_tokens = []
    nesting = None
    for token in tokens[::-1]:
        if nesting is not None:
            if nesting < 1:
                if token.type in ('UINT', 'NZUINT'):
                    reversion_tokens.append(token)
                break
        else:
            if token.type == 'RIGHT_PARENS':
                if nesting is None:
                    nesting = 1
                else:
                    nesting = nesting + 1
            elif token.type == 'LEFT_PARENS':
                if nesting is None:
                    raise InvalidFormat('Unbalanced parens in format')
                else:
                    nesting = nesting - 1
        reversion_tokens.append(token)

    reversion_tokens.reverse()
    return reversion_tokens


def _read_quoted_string(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string != 'QUOTED_STRING':
        raise InvalidFormat('Token %s has invalid neighbouring token' % tokens[0])
    ed = QuotedString()
    ed.char_string = tokens[0].value
    return ed


def _read_ed1(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string != 'ED1':
        raise InvalidFormat('Token %s has invalid neighbouring token' % tokens[0])
    ed = get_edit_descriptor_obj(tokens[0].value)
    return ed


def _read_ed2(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string != 'NZUINT,ED2':
        raise InvalidFormat('Token %s has invalid neighbouring token' % tokens[0])
    ed = get_edit_descriptor_obj(tokens[1].value)
    ed.num_chars = tokens[0].value
    return ed


def _read_ed3(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string != 'ED3,NZUINT':
        raise InvalidFormat('Token %s has invalid neighbouring token' % tokens[0])
    else:
        ed = get_edit_descriptor_obj(tokens[0].value)
        if hasattr(ed, 'width'):
            ed.width = tokens[1].value
        else:
            ed.num_chars = tokens[1].value
    return ed


def _read_ed4(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string in ('ED4', 'ED4,NZUINT') or config.ALLOW_ZERO_WIDTH_EDS and type_string == 'ED4,UINT':
        ed = get_edit_descriptor_obj(tokens[0].value)
        if len(tokens) > 1:
            ed.width = tokens[1].value
    else:
        raise InvalidFormat('Token %s has invalid neighbouring token' % tokens[0])
    return ed


def _read_ed5(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string in ('ED5,NZUINT,DOT,UINT', 'ED5,NZUINT,DOT,NZUINT') or config.ALLOW_ZERO_WIDTH_EDS and type_string in ('ED5,UINT,DOT,UINT',
                                                                                                                          'ED5,UINT,DOT,NZUINT'):
        ed = get_edit_descriptor_obj(tokens[0].value)
        ed.width = tokens[1].value
        ed.decimal_places = tokens[3].value
    else:
        raise InvalidFormat('%s has invalid neighbouring token' % tokens[0])
    return ed


def _read_ed6(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string == 'ED6,NZUINT' or config.ALLOW_ZERO_WIDTH_EDS and type_string == 'ED6,UINT':
        ed = get_edit_descriptor_obj(tokens[0].value)
        ed.width = tokens[1].value
        ed.min_digits = None
    else:
        if type_string in ('ED6,NZUINT,DOT,UINT', 'ED6,NZUINT,DOT,NZUINT') or config.ALLOW_ZERO_WIDTH_EDS and type_string in ('ED6,UINT,DOT,UINT',
                                                                                                                              'ED6,UINT,DOT,NZUINT'):
            ed = get_edit_descriptor_obj(tokens[0].value)
            ed.width = tokens[1].value
            ed.min_digits = tokens[3].value
        else:
            raise InvalidFormat('%s has invalid neighbouring token' % tokens[0])
    return ed


def _read_ed7(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string in ('ED7,NZUINT,DOT,UINT', 'ED7,NZUINT,DOT,NZUINT') or config.ALLOW_ZERO_WIDTH_EDS and type_string in ('ED7,UINT,DOT,UINT',
                                                                                                                          'ED7,UINT,DOT,NZUINT'):
        ed = get_edit_descriptor_obj(tokens[0].value)
        ed.width = tokens[1].value
        ed.decimal_places = tokens[3].value
        ed.exponent = None
    else:
        if type_string in ('ED7,NZUINT,DOT,NZUINT,ED7,NZUINT', 'ED7,NZUINT,DOT,NZUINT,ED7,UINT',
                           'ED7,NZUINT,DOT,NZUINT,ED7,INT', 'ED7,NZUINT,DOT,UINT,ED7,NZUINT',
                           'ED7,NZUINT,DOT,UINT,ED7,UINT', 'ED7,NZUINT,DOT,UINT,ED7,INT') or config.ALLOW_ZERO_WIDTH_EDS and type_string in ('ED7,UINT,DOT,NZUINT,ED7,NZUINT',
                                                                                                                                             'ED7,UINT,DOT,NZUINT,ED7,UINT',
                                                                                                                                             'ED7,UINT,DOT,NZUINT,ED7,INT',
                                                                                                                                             'ED7,UINT,DOT,UINT,ED7,NZUINT',
                                                                                                                                             'ED7,UINT,DOT,UINT,ED7,UINT',
                                                                                                                                             'ED7,UINT,DOT,UINT,ED7,INT'):
            ed = get_edit_descriptor_obj(tokens[0].value)
            ed.width = tokens[1].value
            ed.decimal_places = tokens[3].value
            ed.exponent = tokens[5].value
        else:
            raise InvalidFormat('%s has invalid neighbouring token' % tokens[0])
    return ed


def _read_ed8(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string in ('NZUINT,ED8', 'UINT,ED8', 'INT,ED8'):
        ed = get_edit_descriptor_obj(tokens[1].value)
        ed.scale = tokens[0].value
    else:
        raise InvalidFormat('%s has invalid neighbouring token' % tokens[0])
    return ed


def _read_ed9(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string == 'ED9':
        ed = get_edit_descriptor_obj(tokens[0].value)
    else:
        raise InvalidFormat('%s has invalid neighbouring token' % tokens[0])
    return ed


def _read_ed10(tokens):
    type_string = ','.join([t.type for t in tokens])
    if type_string == 'ED10':
        ed = get_edit_descriptor_obj(tokens[0].value)
    else:
        raise InvalidFormat('%s has invalid neighbouring token' % tokens[0])
    return ed


def _remove_outer_parens(tokens):
    if tokens[0].type == 'LEFT_PARENS':
        if tokens[(-1)].type == 'RIGHT_PARENS':
            tokens = tokens[1:-1]
    return tokens