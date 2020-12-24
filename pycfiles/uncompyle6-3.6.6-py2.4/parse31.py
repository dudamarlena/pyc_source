# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse31.py
# Compiled at: 2020-04-20 22:50:15
"""
spark grammar differences over Python 3.2 for Python 3.1.
"""
from uncompyle6.parser import PythonParserSingle
from uncompyle6.parsers.parse32 import Python32Parser

class Python31Parser(Python32Parser):
    __module__ = __name__

    def p_31(self, args):
        """
        subscript2     ::= expr expr DUP_TOPX BINARY_SUBSCR

        setupwith      ::= DUP_TOP LOAD_ATTR store LOAD_ATTR CALL_FUNCTION_0 POP_TOP
        setupwithas    ::= DUP_TOP LOAD_ATTR store LOAD_ATTR CALL_FUNCTION_0 store
        with           ::= expr setupwith SETUP_FINALLY
                           suite_stmts_opt
                           POP_BLOCK LOAD_CONST COME_FROM_FINALLY
                           load del_stmt WITH_CLEANUP END_FINALLY

        # Keeps Python 3.1 withas desigator in the same position as it is in other version
        setupwithas31  ::= setupwithas SETUP_FINALLY load del_stmt

        withasstmt     ::= expr setupwithas31 store
                           suite_stmts_opt
                           POP_BLOCK LOAD_CONST COME_FROM_FINALLY
                           load del_stmt WITH_CLEANUP END_FINALLY

        store ::= STORE_NAME
        load  ::= LOAD_FAST
        load  ::= LOAD_NAME
        """
        pass

    def remove_rules_31(self):
        self.remove_rules('\n        # DUP_TOP_TWO is DUP_TOPX in 3.1 and earlier\n        subscript2 ::= expr expr DUP_TOP_TWO BINARY_SUBSCR\n\n        # The were found using grammar coverage\n        list_if     ::= expr jmp_false list_iter COME_FROM\n        list_if_not ::= expr jmp_true list_iter COME_FROM\n        ')

    def customize_grammar_rules(self, tokens, customize):
        super(Python31Parser, self).customize_grammar_rules(tokens, customize)
        self.remove_rules_31()


class Python31ParserSingle(Python31Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python31Parser()
    p.remove_rules_31()
    p.check_grammar()
    from uncompyle6 import PYTHON_VERSION, IS_PYPY
    if PYTHON_VERSION == 3.1:
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
        import sys
        if len(sys.argv) > 1:
            from spark_parser.spark import rule2str
            for rule in sorted(p.rule2name.items()):
                print rule2str(rule[0])