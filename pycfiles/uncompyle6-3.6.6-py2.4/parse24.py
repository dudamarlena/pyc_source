# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse24.py
# Compiled at: 2020-04-20 22:50:15
"""
spark grammar differences over Python2.5 for Python 2.4.
"""
from uncompyle6.parser import PythonParserSingle
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parsers.parse25 import Python25Parser

class Python24Parser(Python25Parser):
    __module__ = __name__

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python24Parser, self).__init__(debug_parser)
        self.customized = {}

    def p_misc24(self, args):
        """
        # Python 2.4 only adds something like the below for if 1:
        # However we will just treat it as a noop (which of course messes up
        # simple verify of bytecode.
        # See also below in reduce_is_invalid where we check that the JUMP_FORWARD
        # target matches the COME_FROM target
        stmt     ::= nop_stmt
        nop_stmt ::= JUMP_FORWARD POP_TOP COME_FROM

        # 2.5+ has two LOAD_CONSTs, one for the number '.'s in a relative import
        # keep positions similar to simplify semantic actions

        import           ::= filler LOAD_CONST alias
        import_from      ::= filler LOAD_CONST IMPORT_NAME importlist POP_TOP
        import_from_star ::= filler LOAD_CONST IMPORT_NAME IMPORT_STAR

        importmultiple ::= filler LOAD_CONST alias imports_cont
        import_cont    ::= filler LOAD_CONST alias

        # Handle "if true else: ..." in Python 2.4
        stmt            ::= iftrue_stmt24
        iftrue_stmt24   ::= _ifstmts_jump24 suite_stmts COME_FROM
        _ifstmts_jump24 ::= c_stmts_opt JUMP_FORWARD POP_TOP

        # Python 2.5+ omits POP_TOP POP_BLOCK
        while1stmt ::= SETUP_LOOP l_stmts_opt JUMP_BACK
                       POP_TOP POP_BLOCK COME_FROM
        while1stmt ::= SETUP_LOOP l_stmts_opt JUMP_BACK
                       POP_TOP POP_BLOCK
        while1stmt ::= SETUP_LOOP l_stmts COME_FROM JUMP_BACK
                       POP_TOP POP_BLOCK COME_FROM

        continue   ::= JUMP_BACK JUMP_ABSOLUTE

        # Python 2.4
        # The following has no "JUMP_BACK" after l_stmts because
        # l_stmts ends in a "break", "return", or "continue"
        while1stmt ::= SETUP_LOOP l_stmts
                       POP_TOP POP_BLOCK

        # Python 2.5+:
        #  call_stmt ::= expr POP_TOP
        #  expr      ::= yield
        call_stmt ::= yield

        # Python 2.5+ adds POP_TOP at the end
        gen_comp_body ::= expr YIELD_VALUE

        # Python 2.4
        # Python 2.6, 2.7 and 3.3+ use kv3
        # Python 2.3- use kv
        kvlist ::= kvlist kv2
        kv2    ::= DUP_TOP expr expr ROT_THREE STORE_SUBSCR
        """
        pass

    def remove_rules_24(self):
        self.remove_rules('\n        expr ::= if_exp\n        ')

    def customize_grammar_rules(self, tokens, customize):
        self.remove_rules('\n        gen_comp_body ::= expr YIELD_VALUE POP_TOP\n        kvlist        ::= kvlist kv3\n        while1stmt    ::= SETUP_LOOP l_stmts JUMP_BACK COME_FROM\n        while1stmt    ::= SETUP_LOOP l_stmts_opt JUMP_BACK COME_FROM\n        while1stmt    ::= SETUP_LOOP returns COME_FROM\n        whilestmt     ::= SETUP_LOOP testexpr returns POP_BLOCK COME_FROM\n        with_cleanup  ::= LOAD_FAST DELETE_FAST WITH_CLEANUP END_FINALLY\n        with_cleanup  ::= LOAD_NAME DELETE_NAME WITH_CLEANUP END_FINALLY\n        withasstmt    ::= expr setupwithas store suite_stmts_opt POP_BLOCK LOAD_CONST COME_FROM with_cleanup\n        with          ::= expr setupwith SETUP_FINALLY suite_stmts_opt POP_BLOCK LOAD_CONST COME_FROM with_cleanup\n        stmt ::= with\n        stmt ::= withasstmt\n        ')
        super(Python24Parser, self).customize_grammar_rules(tokens, customize)
        self.remove_rules_24()
        if self.version == 2.4:
            self.check_reduce['nop_stmt'] = 'tokens'

    def reduce_is_invalid(self, rule, ast, tokens, first, last):
        invalid = super(Python24Parser, self).reduce_is_invalid(rule, ast, tokens, first, last)
        if invalid or tokens is None:
            return invalid
        lhs = rule[0]
        if lhs == 'nop_stmt':
            l = len(tokens)
            if 0 <= l < len(tokens):
                return not int(tokens[first].pattr) == tokens[last].offset
        return False


class Python24ParserSingle(Python24Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python24Parser()
    p.check_grammar()