# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/lexer/delim_lexer.py
# Compiled at: 2019-12-17 01:13:16
# Size of source mod 2**32: 6780 bytes
import re
from future.utils import lfilter, lmap
from ply import lex
from itertools import chain
from foxylib.tools.lexer.lexer_tools import LexerToolkit, MultipleColonInCommandError as MCICErr
from foxylib.tools.collections.collections_tool import lchain
from foxylib.tools.string.string_tool import str2strip

class DelimLexer(object):
    tokens = ('DQ', 'SQ', 'BACKSLASH', 'DELIM', 'ANY')
    t_SQ = "'"
    t_DQ = '"'
    t_BACKSLASH = '\\\\'

    @classmethod
    def chariter2r_ANY(cls, l):
        return '[{0}]'.format(''.join(map(re.escape, l)))

    @classmethod
    def chariter2r_NONE(cls, l):
        return '[^{0}]+'.format(''.join(map(re.escape, l)))

    @classmethod
    def specialchars(cls):
        return ''.join(["'", '"', '\\'])

    def t_DELIM(self, t):
        return t

    def t_ANY(self, t):
        return t

    def t_error(self, t):
        raise Exception("Illegal character '%s'" % t.value[0])

    def build(self, **kwargs):
        self.lexer = (lex.lex)(module=self, **kwargs)

    @classmethod
    def r_TUPLE2lexer(cls, r_TUPLE):
        m = cls()
        cls.t_DELIM.regex, cls.t_ANY.regex = r_TUPLE
        m.build()
        lexer = m.lexer
        return lexer

    @classmethod
    def lexer_args(cls):
        s_delim_eaters = ','
        s_ANY_EXs = lchain(s_delim_eaters, DelimLexer.specialchars())
        r_TUPLE = ('\\s+',
         '(?:(?:[^\\s{0}])|(?:{1}))'.format(''.join(map(re.escape, s_ANY_EXs)), '\\s*(?:{0})\\s*'.format('|'.join(map(re.escape, s_delim_eaters)))))
        lexer = cls.r_TUPLE2lexer(r_TUPLE)
        return lexer

    @classmethod
    def str_DELIMs2lexer(cls, str_DELIMs):
        r_TUPLE = (DelimLexer.chariter2r_ANY(str_DELIMs),
         DelimLexer.chariter2r_NONE(chain(DelimLexer.specialchars(), str_DELIMs)))
        lexer = cls.r_TUPLE2lexer(r_TUPLE)
        return lexer

    @classmethod
    def str2s_INSTR_list(cls, s_IN, delim_HEAD=None, delim_INSTR=None):
        if delim_HEAD is None:
            delim_HEAD = ':'
        else:
            if delim_INSTR is None:
                delim_INSTR = ';'
            s_COLON_list = DelimLexer.lexer2str_DELIM_list(cls.str_DELIMs2lexer(delim_HEAD), LexerToolkit.DELIM_EXCLUDED, s_IN)
            MCICErr.chk_n_raise(s_COLON_list, s_IN)
            return s_COLON_list or s_COLON_list
        s_SEMI_list_RAW = DelimLexer.lexer2str_DELIM_list(cls.str_DELIMs2lexer(delim_INSTR), LexerToolkit.DELIM_EXCLUDED, s_COLON_list[(-1)])
        s_SEMI_list = lfilter(bool, map(lambda x: x.strip(), s_SEMI_list_RAW))
        if len(s_COLON_list) == 1:
            return s_SEMI_list
        l = [' '.join([s_COLON_list[0], s_SEMI]) for s_SEMI in s_SEMI_list]
        return l

    @classmethod
    def str2s_COMMA_list(cls, s_IN):
        l = DelimLexer.lexer2str_DELIM_list(cls.str_DELIMs2lexer(','), LexerToolkit.DELIM_EXCLUDED, s_IN)
        s_COMMA_list = lmap(str2strip, l)
        return s_COMMA_list

    @classmethod
    def lexer2str_DELIM_list(cls, lexer, delim_rule, s_IN, maxsplit=None):
        lexer.input(s_IN)
        tt_list_ESCAPE = [
         'BACKSLASH']
        tt_list_STATE = [
         'DQ']
        tt_list_DELIM = ['DELIM']
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
            is_append_BEFORE = all([tok.type not in tt_list_STATE,
             any([stt not in [LexerToolkit.STT_DELIM],
              delim_rule in [LexerToolkit.DELIM_AS_SUFFIX]])])
            is_append_BEFORE_and_done = stt in [LexerToolkit.STT_ANY]
            if is_append_BEFORE:
                token_list_DELIM.append(tok)
            if is_append_BEFORE_and_done:
                continue
            if stt == LexerToolkit.STT_DELIM:
                create_str_DELIM = True
                if create_str_DELIM:
                    str_DELIM_list.append(LexerToolkit.token_list_DELIM2str_DELIM(token_list_DELIM))
                    token_list_DELIM = []
                if delim_rule in [LexerToolkit.DELIM_AS_PREFIX]:
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


def main():
    s_IN = '"a1{0} a2"{0} b1 b2{0} "c1 c2" c3{0} d1'.format(';')
    l = DelimLexer.lexer2str_DELIM_list(DelimLexer.str_DELIMs2lexer(';'), LexerToolkit.DELIM_AS_SUFFIX, s_IN)
    print(l)


if __name__ == '__main__':
    main()