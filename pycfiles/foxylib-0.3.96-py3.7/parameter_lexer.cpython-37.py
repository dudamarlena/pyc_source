# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/lexer/parameter_lexer.py
# Compiled at: 2019-12-17 01:13:16
# Size of source mod 2**32: 7439 bytes
import re
from future.utils import lmap, lfilter
from ply import lex
from foxylib.tools.collections.collections_tool import lchain
from foxylib.tools.lexer.lexer_tools import LexerToolkit
from foxylib.tools.string.string_tool import str2strip

class ParameterLexer(object):
    tokens = ('ANY', 'DQ', 'SQ', 'BACKSLASH', 'EQUAL', 'DELIM_PREFIX')
    l_PREFIX = [
     '+', '-', '*', '?']
    t_DQ = '"'
    t_SQ = "'"
    t_BACKSLASH = '\\\\'
    t_EQUAL = '='
    t_DELIM_PREFIX = '[{0}]'.format(''.join(lmap(re.escape, l_PREFIX)))
    l_VAR = lchain(l_PREFIX, ['\\', '=', "'", '"'])
    t_ANY = '(?:[^\\s{0}]+)|(?:\\s+)'.format(''.join(lmap(re.escape, l_VAR)))

    def t_error(self, t):
        raise Exception("Illegal character '%s'" % t.value[0])

    def build(self, **kwargs):
        self.lexer = (lex.lex)(module=self, **kwargs)

    DELIM_TYPE_PREFIX = 'P'
    DELIM_TYPE_INFIX = 'I'

    @classmethod
    def r_prefix(cls):
        return '(?:{0})'.format('|'.join(lmap(re.escape, cls.l_PREFIX)))

    @classmethod
    def stt_delim2type(cls, tok):
        is_PREFIX = tok.value in cls.l_PREFIX
        is_INFIX = tok.value in ('=', )
        if len(lfilter(bool, [is_PREFIX, is_INFIX])) != 1:
            raise Exception()
        if is_PREFIX:
            return cls.DELIM_TYPE_PREFIX
        if is_INFIX:
            return cls.DELIM_TYPE_INFIX
        raise Exception()

    @classmethod
    def delim_infix2iStart(cls, token_list_DELIM, tt_list_DELIM):
        if not token_list_DELIM:
            return
        tok_LAST = token_list_DELIM[(-1)]
        if tok_LAST.type != 'ANY':
            return
        if len(token_list_DELIM) <= 1:
            return -1
        tok_2PREV = token_list_DELIM[(-2)]
        if tok_2PREV.type not in tt_list_DELIM:
            return -1
        delim_type = cls.stt_delim2type(tok_2PREV)
        if delim_type == cls.DELIM_TYPE_INFIX:
            return
        if delim_type == cls.DELIM_TYPE_PREFIX:
            return -2
        raise Exception()

    @classmethod
    def is_delim_infix_valid(cls, token_list_DELIM):
        if not token_list_DELIM:
            return False
        tok_LAST = token_list_DELIM[(-1)]
        if tok_LAST.type != 'ANY':
            return False
        return True

    @classmethod
    def lexer2str_DELIM_list(cls, lexer, s_IN, maxsplit=None):
        lexer.input(s_IN)
        tt_list_ESCAPE = [
         'BACKSLASH']
        tt_list_STATE = ['SQ', 'DQ']
        tt_list_DELIM = ['DELIM_PREFIX', 'EQUAL']
        str_DELIM_list = []
        token_list_DELIM = []
        state_INITIAL = 'INITIAL'
        l_state = [state_INITIAL]
        while 1:
            tok = lexer.token()
            if not tok:
                break
            state_CUR = l_state[(-1)]
            stop_split = maxsplit is not None and len(str_DELIM_list) >= maxsplit
            stt = LexerToolkit.tok2semantic_token_type(tok, token_list_DELIM, [
             tt_list_ESCAPE, tt_list_STATE, tt_list_DELIM], stop_split, state_CUR, state_INITIAL)
            is_append_BEFORE = stt not in [LexerToolkit.STT_DELIM]
            is_append_BEFORE_and_done = stt in [LexerToolkit.STT_ANY]
            if is_append_BEFORE:
                token_list_DELIM.append(tok)
            if is_append_BEFORE_and_done:
                continue
            if stt == LexerToolkit.STT_DELIM:
                delim_type = cls.stt_delim2type(tok)
                if delim_type == cls.DELIM_TYPE_INFIX:
                    iSTART_INFIX = cls.delim_infix2iStart(token_list_DELIM, tt_list_DELIM)
                    if iSTART_INFIX is None:
                        return
                    if iSTART_INFIX < -1:
                        if len(token_list_DELIM) != 2:
                            raise Exception()
                    else:
                        token_list_PREV = token_list_DELIM[:iSTART_INFIX]
                        str_DELIM_list.append(LexerToolkit.token_list_DELIM2str_DELIM(token_list_PREV))
                        token_list_DELIM = token_list_DELIM[iSTART_INFIX:]
                else:
                    if delim_type == cls.DELIM_TYPE_PREFIX:
                        token_list_PREV = token_list_DELIM
                        str_DELIM_list.append(LexerToolkit.token_list_DELIM2str_DELIM(token_list_PREV))
                        token_list_DELIM = []
                    else:
                        raise Exception()
                token_list_DELIM.append(tok)
                continue
            if stt == LexerToolkit.STT_START:
                l_state.append(tok.type)
                continue
            if stt == LexerToolkit.STT_END:
                if l_state[(-1)] != tok.type:
                    raise Exception()
                l_state.pop()
                continue

        if len(l_state) > 1:
            return
        if l_state[0] != state_INITIAL:
            return
        if token_list_DELIM:
            str_DELIM_list.append(LexerToolkit.token_list_DELIM2str_DELIM(token_list_DELIM))
        return str_DELIM_list

    @classmethod
    def str2l_token(cls, s, maxsplit=None, include_tokens=None):
        if include_tokens is None:
            include_tokens = True
        m = cls()
        m.build()
        tok_groups = (
         [
          'ANY', 'SINGLEQUOTE', 'DOUBLEQUOTE'],
         [
          'DELIM'])
        l = LexerToolkit.str2str_token_list((m.lexer), s, tok_groups, maxsplit=maxsplit, include_tokens=include_tokens)
        return l

    @classmethod
    def create_lexer(cls):
        m = cls()
        m.build()
        lexer = m.lexer
        return lexer

    @classmethod
    def str2args_kwargs_pair(cls, s_IN, maxsplit=None):
        str_PARAM_list = cls.lexer2str_DELIM_list((cls.create_lexer()), s_IN,
          maxsplit=maxsplit)
        if not str_PARAM_list:
            return (
             None, str_PARAM_list)
        return (str2strip(str_PARAM_list[0]),
         lmap(str2strip, str_PARAM_list[1:]))

    @classmethod
    def str2args_kwargs_pair_NEW(cls, s_IN, split_ARG_str):
        str_PARAM_list = cls.lexer2str_DELIM_list(cls.create_lexer(), s_IN)
        if not str_PARAM_list:
            return (
             None, str_PARAM_list)
        return (str2strip(str_PARAM_list[0]),
         lmap(str2strip, str_PARAM_list[1:]))