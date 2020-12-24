# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse25.py
# Compiled at: 2020-04-20 22:50:15
"""
spark grammar differences over Python2.6 for Python 2.5.
"""
from uncompyle6.parser import PythonParserSingle
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parsers.parse26 import Python26Parser
from uncompyle6.parsers.reducecheck import ifelsestmt

class Python25Parser(Python26Parser):
    __module__ = __name__

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python25Parser, self).__init__(debug_parser)
        self.customized = {}

    def p_misc25(self, args):
        """
        # If "return_if_stmt" is in a loop, a JUMP_BACK can be emitted. In 2.6 the
        # JUMP_BACK doesn't appear

        return_if_stmt ::= ret_expr  RETURN_END_IF JUMP_BACK

        # We have no jumps to jumps, so no "come_froms" but a single "COME_FROM"
        ifelsestmt ::= testexpr c_stmts_opt jf_cf_pop else_suite COME_FROM

        # Python 2.6 uses ROT_TWO instead of the STORE_xxx
        # withas is allowed as a "from future" in 2.5
        # 2.6 and 2.7 do something slightly different
        setupwithas ::= DUP_TOP LOAD_ATTR store LOAD_ATTR CALL_FUNCTION_0
                        setup_finally
        # opcode SETUP_WITH
        setupwith ::= DUP_TOP LOAD_ATTR store LOAD_ATTR CALL_FUNCTION_0 POP_TOP
        with      ::= expr setupwith SETUP_FINALLY suite_stmts_opt
                      POP_BLOCK LOAD_CONST COME_FROM with_cleanup

        # Semantic actions want store to be at index 2
        withasstmt ::= expr setupwithas store suite_stmts_opt
                       POP_BLOCK LOAD_CONST COME_FROM with_cleanup

        store ::= STORE_NAME
        store ::= STORE_FAST

        # tryelsetmtl doesn't need COME_FROM since the jump might not
        # be the the join point at the end of the "try" but instead back to the
        # loop. FIXME: should "come_froms" below be a single COME_FROM?
        tryelsestmt    ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                           except_handler else_suite come_froms
        tryelsestmtl   ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                            except_handler else_suitel

        # Python 2.6 omits the LOAD_FAST DELETE_FAST below
        # withas is allowed as a "from future" in 2.5
        withasstmt ::= expr setupwithas store suite_stmts_opt
                       POP_BLOCK LOAD_CONST COME_FROM
                       with_cleanup

        with_cleanup ::= LOAD_FAST DELETE_FAST WITH_CLEANUP END_FINALLY
        with_cleanup ::= LOAD_NAME DELETE_NAME WITH_CLEANUP END_FINALLY

        kvlist ::= kvlist kv
        kv     ::= DUP_TOP expr ROT_TWO expr STORE_SUBSCR
        """
        pass

    def customize_grammar_rules(self, tokens, customize):
        self.remove_rules('\n        # No jump to jumps in 2.4 so we have a single "COME_FROM", not "come_froms"\n        ifelsestmt    ::= testexpr c_stmts_opt jf_cf_pop else_suite come_froms\n\n        setupwith  ::= DUP_TOP LOAD_ATTR ROT_TWO LOAD_ATTR CALL_FUNCTION_0 POP_TOP\n        with       ::= expr setupwith SETUP_FINALLY suite_stmts_opt\n                       POP_BLOCK LOAD_CONST COME_FROM WITH_CLEANUP END_FINALLY\n        withasstmt ::= expr setupwithas store suite_stmts_opt\n                       POP_BLOCK LOAD_CONST COME_FROM WITH_CLEANUP END_FINALLY\n        assert2       ::= assert_expr jmp_true LOAD_ASSERT expr CALL_FUNCTION_1 RAISE_VARARGS_1\n        classdefdeco  ::= classdefdeco1 store\n        classdefdeco1 ::= expr classdefdeco1 CALL_FUNCTION_1\n        classdefdeco1 ::= expr classdefdeco2 CALL_FUNCTION_1\n        classdefdeco2 ::= LOAD_CONST expr mkfunc CALL_FUNCTION_0 BUILD_CLASS\n        kv3 ::= expr expr STORE_MAP\n        if_exp_ret       ::= expr jmp_false_then expr RETURN_END_IF POP_TOP ret_expr_or_cond\n        return_if_lambda ::= RETURN_END_IF_LAMBDA POP_TOP\n        return_if_stmt   ::= ret_expr RETURN_END_IF POP_TOP\n        return_if_stmts  ::= return_if_stmt\n        return           ::= ret_expr RETURN_END_IF POP_TOP\n        return           ::= ret_expr RETURN_VALUE POP_TOP\n        return_stmt_lambda ::= ret_expr RETURN_VALUE_LAMBDA\n        setupwithas      ::= DUP_TOP LOAD_ATTR ROT_TWO LOAD_ATTR CALL_FUNCTION_0 setup_finally\n        stmt             ::= classdefdeco\n        stmt             ::= if_exp_lambda\n        stmt             ::= if_exp_not_lambda\n        if_exp_lambda    ::= expr jmp_false_then expr return_if_lambda\n                               return_stmt_lambda LAMBDA_MARKER\n        if_exp_not_lambda ::= expr jmp_true_then expr return_if_lambda\n                              return_stmt_lambda LAMBDA_MARKER\n        ')
        super(Python25Parser, self).customize_grammar_rules(tokens, customize)
        if self.version == 2.5:
            self.check_reduce['try_except'] = 'tokens'
        self.check_reduce['aug_assign1'] = 'AST'
        self.check_reduce['ifelsestmt'] = 'AST'

    def reduce_is_invalid(self, rule, ast, tokens, first, last):
        invalid = super(Python25Parser, self).reduce_is_invalid(rule, ast, tokens, first, last)
        if invalid or tokens is None:
            return invalid
        if rule == ('aug_assign1', ('expr', 'expr', 'inplace_op', 'store')):
            return ast[0][0] == 'and'
        lhs = rule[0]
        n = len(tokens)
        if lhs == 'ifelsestmt':
            return ifelsestmt(self, lhs, n, rule, ast, tokens, first, last)
        return False


class Python25ParserSingle(Python26Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python25Parser()
    p.check_grammar()