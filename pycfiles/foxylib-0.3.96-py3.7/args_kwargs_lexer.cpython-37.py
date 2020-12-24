# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/lexer/args_kwargs_lexer.py
# Compiled at: 2019-12-17 01:13:16
# Size of source mod 2**32: 9945 bytes
import re
from future.utils import lmap
from ply import lex
from foxylib.tools.lexer.delim_lexer import DelimLexer
from foxylib.tools.lexer.lexer_tools import LexerToolkit
from foxylib.tools.string.string_tool import str2strip, StringTool

class ArgsKwargsLexer(object):
    tokens = ('ANY', 'WHITESPACE', 'DQ', 'SQ', 'BACKSLASH', 'EQUAL')
    t_DQ = '"'
    t_SQ = "'"
    t_BACKSLASH = '\\\\'
    t_EQUAL = '='
    l_VAR = [
     '\\', '=', "'", '"']
    t_WHITESPACE = '\\s+'
    t_ANY = '(?:[^\\s{0}]+)'.format(''.join(lmap(re.escape, l_VAR)))

    def t_error(self, t):
        raise Exception("Illegal character '%s'" % t.value[0])

    def build(self, **kwargs):
        self.lexer = (lex.lex)(module=self, **kwargs)

    @classmethod
    def delim_infix2iStart(cls, token_list_DELIM, tt_list_DELIM):
        if not token_list_DELIM:
            return
        iStart = -1
        while 1:
            if abs(iStart) > len(token_list_DELIM):
                return iStart + 1
            token_CUR = token_list_DELIM[iStart]
            if token_CUR.type == 'WHITESPACE':
                iStart -= 1
                continue
            if token_CUR.type in tt_list_DELIM:
                return
            return iStart

    @classmethod
    def lexer2str_DELIM_list(cls, lexer, s_IN, maxsplit=None):
        lexer.input(s_IN)
        tt_list_ESCAPE = [
         'BACKSLASH']
        tt_list_STATE = ['SQ', 'DQ']
        tt_list_DELIM = ['EQUAL']
        l_OUT = []
        token_list_DELIM = []
        state_INITIAL = 'INITIAL'
        l_state = [state_INITIAL]
        while 1:
            tok = lexer.token()
            if not tok:
                break
            state_CUR = l_state[(-1)]
            stop_split = maxsplit is not None and len(l_OUT) >= maxsplit
            stt = LexerToolkit.tok2semantic_token_type(tok, token_list_DELIM, [
             tt_list_ESCAPE, tt_list_STATE, tt_list_DELIM], stop_split, state_CUR, state_INITIAL)
            is_append_BEFORE = stt not in [LexerToolkit.STT_DELIM]
            is_append_BEFORE_and_done = stt in [LexerToolkit.STT_ANY]
            if is_append_BEFORE:
                token_list_DELIM.append(tok)
            if is_append_BEFORE_and_done:
                continue
            if stt == LexerToolkit.STT_DELIM:
                iSTART_INFIX = cls.delim_infix2iStart(token_list_DELIM, tt_list_DELIM)
                if iSTART_INFIX is None:
                    return
                token_list_PREV = token_list_DELIM[:iSTART_INFIX]
                l_OUT.append(LexerToolkit.token_list_DELIM2str_DELIM(token_list_PREV))
                token_list_DELIM = token_list_DELIM[iSTART_INFIX:]
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
            l_OUT.append(LexerToolkit.token_list_DELIM2str_DELIM(token_list_DELIM))
        return l_OUT

    class SyntacticError(Exception):
        pass

    @classmethod
    def _lexer2str_ARGs_h_KWARG(cls, lexer, s_IN):
        lexer.input(s_IN)
        tt_list_ESCAPE = [
         'BACKSLASH']
        tt_list_STATE = ['SQ', 'DQ']
        tt_list_DELIM = ['EQUAL']
        str_ARGs, h_KWARG = None, {}
        kwarg_KEY = None
        token_list_DELIM = []
        state_INITIAL = 'INITIAL'
        l_state = [state_INITIAL]
        while 1:
            tok = lexer.token()
            if not tok:
                break
            state_CUR = l_state[(-1)]
            stt = LexerToolkit.tok2semantic_token_type(tok, token_list_DELIM, [
             tt_list_ESCAPE, tt_list_STATE, tt_list_DELIM], False, state_CUR, state_INITIAL)
            is_append_BEFORE = stt not in [LexerToolkit.STT_DELIM]
            is_append_BEFORE_and_done = stt in [LexerToolkit.STT_ANY]
            if is_append_BEFORE:
                token_list_DELIM.append(tok)
            if is_append_BEFORE_and_done:
                continue
            if stt == LexerToolkit.STT_DELIM:
                iSTART_INFIX = cls.delim_infix2iStart(token_list_DELIM, tt_list_DELIM)
                if iSTART_INFIX is None:
                    raise cls.SyntacticError()
                str_PREV = str2strip(LexerToolkit.token_list_DELIM2str_DELIM(token_list_DELIM[:iSTART_INFIX]))
                str_ARGs_THIS = cls._zzz(str_PREV, kwarg_KEY, h_KWARG)
                if str_ARGs_THIS:
                    if str_ARGs is not None:
                        raise cls.SyntacticError()
                    str_ARGs = str_ARGs_THIS
                kwarg_KEY = LexerToolkit.token_list_DELIM2str_DELIM(token_list_DELIM[iSTART_INFIX:])
                token_list_DELIM = []
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
            str_PREV = str2strip(LexerToolkit.token_list_DELIM2str_DELIM(token_list_DELIM))
            str_ARGs_THIS = cls._zzz(str_PREV, kwarg_KEY, h_KWARG)
            if str_ARGs_THIS:
                if str_ARGs is not None:
                    raise cls.SyntacticError()
                str_ARGs = str_ARGs_THIS
        return (
         str_ARGs, h_KWARG)

    @classmethod
    def _zzz(cls, str_PREV, kwarg_KEY, h_KWARG):
        str_ARGs = None
        if not kwarg_KEY:
            if str_PREV:
                str_ARGs = str_PREV
        else:
            if not str_PREV:
                raise cls.SyntacticError()
            h_KWARG[StringTool.quoted2stripped(kwarg_KEY.strip())] = StringTool.quoted2stripped(str_PREV.strip())
        return str_ARGs

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
    def str2args_kwargs_pair(cls, s_IN, max_args_count=None):
        str_ARGs, h_KWARG = cls._lexer2str_ARGs_h_KWARG(cls.create_lexer(), str2strip(s_IN))
        if not str_ARGs:
            arg_list = []
        else:
            maxsplit = max_args_count - 1 if max_args_count else max_args_count
            l = DelimLexer.lexer2str_DELIM_list((DelimLexer.lexer_args()), (LexerToolkit.DELIM_EXCLUDED),
              str_ARGs,
              maxsplit=maxsplit)
            arg_list = lmap(StringTool.quoted2stripped, lmap(str2strip, l))
        return (
         arg_list, h_KWARG)