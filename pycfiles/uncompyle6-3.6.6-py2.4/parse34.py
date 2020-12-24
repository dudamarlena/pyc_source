# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse34.py
# Compiled at: 2019-11-16 18:01:23
"""
spark grammar differences over Python 3.3 for Python 3.4
"""
from uncompyle6.parser import PythonParserSingle
from uncompyle6.parsers.parse33 import Python33Parser

class Python34Parser(Python33Parser):
    __module__ = __name__

    def p_misc34(self, args):
        """
        expr ::= LOAD_ASSERT

        # passtmt is needed for semantic actions to add "pass"
        suite_stmts_opt ::= pass

        whilestmt     ::= SETUP_LOOP testexpr returns come_froms POP_BLOCK COME_FROM_LOOP

        # Seems to be needed starting 3.4.4 or so
        while1stmt    ::= SETUP_LOOP l_stmts
                          COME_FROM JUMP_BACK POP_BLOCK COME_FROM_LOOP
        while1stmt    ::= SETUP_LOOP l_stmts
                          POP_BLOCK COME_FROM_LOOP

        # FIXME the below masks a bug in not detecting COME_FROM_LOOP
        # grammar rules with COME_FROM -> COME_FROM_LOOP already exist
        whileelsestmt     ::= SETUP_LOOP testexpr l_stmts_opt JUMP_BACK POP_BLOCK
                              else_suitel COME_FROM

        while1elsestmt    ::= SETUP_LOOP l_stmts JUMP_BACK _come_froms POP_BLOCK else_suitel
                              COME_FROM_LOOP

        # Python 3.4+ optimizes the trailing two JUMPS away

        # This is 3.4 only
        yield_from ::= expr GET_ITER LOAD_CONST YIELD_FROM

        _ifstmts_jump ::= c_stmts_opt JUMP_ABSOLUTE JUMP_FORWARD COME_FROM
        """
        pass

    def customize_grammar_rules(self, tokens, customize):
        self.remove_rules('\n        yield_from    ::= expr expr YIELD_FROM\n        # 3.4.2 has this. 3.4.4 may now\n        # while1stmt ::= SETUP_LOOP l_stmts COME_FROM JUMP_BACK COME_FROM_LOOP\n        ')
        super(Python34Parser, self).customize_grammar_rules(tokens, customize)


class Python34ParserSingle(Python34Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python34Parser()
    p.check_grammar()
    from uncompyle6 import PYTHON_VERSION, IS_PYPY
    if PYTHON_VERSION == 3.4:
        (lhs, rhs, tokens, right_recursive, dup_rhs) = p.check_sets()
        from uncompyle6.scanner import get_scanner
        s = get_scanner(PYTHON_VERSION, IS_PYPY)
        opcode_set = set(s.opc.opname).union(set(('JUMP_BACK CONTINUE RETURN_END_IF COME_FROM\n               LOAD_GENEXPR LOAD_ASSERT LOAD_SETCOMP LOAD_DICTCOMP LOAD_CLASSNAME\n               LAMBDA_MARKER RETURN_LAST\n            ').split()))
        remain_tokens = set(tokens) - opcode_set
        import re
        remain_tokens = set([ re.sub('_\\d+$', '', t) for t in remain_tokens ])
        remain_tokens = set([ re.sub('_CONT$', '', t) for t in remain_tokens ])
        remain_tokens = set(remain_tokens) - opcode_set
        print remain_tokens