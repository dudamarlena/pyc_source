# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse36.py
# Compiled at: 2020-04-20 22:50:15
"""
spark grammar differences over Python 3.5 for Python 3.6.
"""
from uncompyle6.parser import PythonParserSingle, nop_func
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parsers.parse35 import Python35Parser
from uncompyle6.scanners.tok import Token

class Python36Parser(Python35Parser):
    __module__ = __name__

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python36Parser, self).__init__(debug_parser)
        self.customized = {}

    def p_36misc(self, args):
        """sstmt ::= sstmt RETURN_LAST

        # long except clauses in a loop can sometimes cause a JUMP_BACK to turn into a
        # JUMP_FORWARD to a JUMP_BACK. And when this happens there is an additional
        # ELSE added to the except_suite. With better flow control perhaps we can
        # sort this out better.
        except_suite ::= c_stmts_opt POP_EXCEPT jump_except ELSE
        except_suite_finalize ::= SETUP_FINALLY c_stmts_opt except_var_finalize END_FINALLY
                                  _jump ELSE

        # 3.6 redoes how return_closure works. FIXME: Isolate to LOAD_CLOSURE
        return_closure   ::= LOAD_CLOSURE DUP_TOP STORE_NAME RETURN_VALUE RETURN_LAST

        for_block       ::= l_stmts_opt come_from_loops JUMP_BACK
        come_from_loops ::= COME_FROM_LOOP*

        whilestmt       ::= SETUP_LOOP testexpr l_stmts_opt
                            JUMP_BACK come_froms POP_BLOCK COME_FROM_LOOP
        whilestmt       ::= SETUP_LOOP testexpr l_stmts_opt
                            come_froms JUMP_BACK come_froms POP_BLOCK COME_FROM_LOOP

        # 3.6 due to jump optimization, we sometimes add RETURN_END_IF where
        # RETURN_VALUE is meant. Specifcally this can happen in
        # ifelsestmt -> ...else_suite _. suite_stmts... (last) stmt
        return ::= ret_expr RETURN_END_IF
        return ::= ret_expr RETURN_VALUE COME_FROM
        return_stmt_lambda ::= ret_expr RETURN_VALUE_LAMBDA COME_FROM

        # A COME_FROM is dropped off because of JUMP-to-JUMP optimization
        and  ::= expr jmp_false expr
        and  ::= expr jmp_false expr jmp_false

        jf_cf       ::= JUMP_FORWARD COME_FROM
        cf_jf_else  ::= come_froms JUMP_FORWARD ELSE

        if_exp ::= expr jmp_false expr jf_cf expr COME_FROM

        async_for_stmt     ::= SETUP_LOOP expr
                               GET_AITER
                               LOAD_CONST YIELD_FROM SETUP_EXCEPT GET_ANEXT LOAD_CONST
                               YIELD_FROM
                               store
                               POP_BLOCK JUMP_FORWARD COME_FROM_EXCEPT DUP_TOP
                               LOAD_GLOBAL COMPARE_OP POP_JUMP_IF_FALSE
                               POP_TOP POP_TOP POP_TOP POP_EXCEPT POP_BLOCK
                               JUMP_ABSOLUTE END_FINALLY COME_FROM
                               for_block POP_BLOCK
                               COME_FROM_LOOP

        stmt      ::= async_for_stmt36

        async_for_stmt36   ::= SETUP_LOOP expr
                               GET_AITER
                               LOAD_CONST YIELD_FROM
                               SETUP_EXCEPT GET_ANEXT LOAD_CONST
                               YIELD_FROM
                               store
                               POP_BLOCK JUMP_BACK COME_FROM_EXCEPT DUP_TOP
                               LOAD_GLOBAL COMPARE_OP POP_JUMP_IF_TRUE
                               END_FINALLY for_block
                               COME_FROM
                               POP_TOP POP_TOP POP_TOP POP_EXCEPT
                               POP_TOP POP_BLOCK
                               COME_FROM_LOOP

        async_forelse_stmt ::= SETUP_LOOP expr
                               GET_AITER
                               LOAD_CONST YIELD_FROM SETUP_EXCEPT GET_ANEXT LOAD_CONST
                               YIELD_FROM
                               store
                               POP_BLOCK JUMP_FORWARD COME_FROM_EXCEPT DUP_TOP
                               LOAD_GLOBAL COMPARE_OP POP_JUMP_IF_FALSE
                               POP_TOP POP_TOP POP_TOP POP_EXCEPT POP_BLOCK
                               JUMP_ABSOLUTE END_FINALLY COME_FROM
                               for_block POP_BLOCK
                               else_suite COME_FROM_LOOP

        # Adds a COME_FROM_ASYNC_WITH over 3.5
        # FIXME: remove corresponding rule for 3.5?

        except_suite ::= c_stmts_opt COME_FROM POP_EXCEPT jump_except COME_FROM

        jb_cfs      ::= JUMP_BACK come_froms

        # If statement inside a loop.
        stmt                ::= ifstmtl
        ifstmtl            ::= testexpr _ifstmts_jumpl
        _ifstmts_jumpl     ::= c_stmts JUMP_BACK

        ifelsestmtl ::= testexpr c_stmts_opt jb_cfs else_suitel
        ifelsestmtl ::= testexpr c_stmts_opt cf_jf_else else_suitel
        ifelsestmt  ::= testexpr c_stmts_opt cf_jf_else else_suite _come_froms
        ifelsestmt  ::= testexpr c_stmts come_froms else_suite come_froms

        # In 3.6+, A sequence of statements ending in a RETURN can cause
        # JUMP_FORWARD END_FINALLY to be omitted from try middle

        except_return    ::= POP_TOP POP_TOP POP_TOP returns
        except_handler   ::= JUMP_FORWARD COME_FROM_EXCEPT except_return

        # Try middle following a returns
        except_handler36 ::= COME_FROM_EXCEPT except_stmts END_FINALLY

        stmt             ::= try_except36
        try_except36     ::= SETUP_EXCEPT returns except_handler36
                             opt_come_from_except
        try_except36     ::= SETUP_EXCEPT suite_stmts
        try_except36     ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                             except_handler36 opt_come_from_except

        # 3.6 omits END_FINALLY sometimes
        except_handler36 ::= COME_FROM_EXCEPT except_stmts
        except_handler36 ::= JUMP_FORWARD COME_FROM_EXCEPT except_stmts
        except_handler   ::= jmp_abs COME_FROM_EXCEPT except_stmts

        stmt             ::= tryfinally36
        tryfinally36     ::= SETUP_FINALLY returns
                             COME_FROM_FINALLY suite_stmts
        tryfinally36     ::= SETUP_FINALLY returns
                             COME_FROM_FINALLY suite_stmts_opt END_FINALLY
        except_suite_finalize ::= SETUP_FINALLY returns
                                  COME_FROM_FINALLY suite_stmts_opt END_FINALLY _jump

        stmt ::= tryfinally_return_stmt
        tryfinally_return_stmt ::= SETUP_FINALLY suite_stmts_opt POP_BLOCK LOAD_CONST
                                   COME_FROM_FINALLY

        compare_chained2 ::= expr COMPARE_OP come_froms JUMP_FORWARD

        """
        pass

    def p_37conditionals(self, args):
        """
        expr                       ::= if_exp37
        if_exp37                   ::= expr expr jf_cfs expr COME_FROM
        jf_cfs                     ::= JUMP_FORWARD _come_froms
        ifelsestmt                 ::= testexpr c_stmts_opt jf_cfs else_suite opt_come_from_except
        """
        pass

    def customize_grammar_rules(self, tokens, customize):
        super(Python36Parser, self).customize_grammar_rules(tokens, customize)
        self.remove_rules('\n           _ifstmts_jumpl     ::= c_stmts_opt\n           _ifstmts_jumpl     ::= _ifstmts_jump\n           except_handler     ::= JUMP_FORWARD COME_FROM_EXCEPT except_stmts END_FINALLY COME_FROM\n           async_for_stmt     ::= SETUP_LOOP expr\n                                  GET_AITER\n                                  LOAD_CONST YIELD_FROM SETUP_EXCEPT GET_ANEXT LOAD_CONST\n                                  YIELD_FROM\n                                  store\n                                  POP_BLOCK jump_except COME_FROM_EXCEPT DUP_TOP\n                                  LOAD_GLOBAL COMPARE_OP POP_JUMP_IF_FALSE\n                                  POP_TOP POP_TOP POP_TOP POP_EXCEPT POP_BLOCK\n                                  JUMP_ABSOLUTE END_FINALLY COME_FROM\n                                  for_block POP_BLOCK JUMP_ABSOLUTE\n                                  COME_FROM_LOOP\n           async_forelse_stmt ::= SETUP_LOOP expr\n                                  GET_AITER\n                                  LOAD_CONST YIELD_FROM SETUP_EXCEPT GET_ANEXT LOAD_CONST\n                                  YIELD_FROM\n                                  store\n                                  POP_BLOCK JUMP_FORWARD COME_FROM_EXCEPT DUP_TOP\n                                  LOAD_GLOBAL COMPARE_OP POP_JUMP_IF_FALSE\n                                  POP_TOP POP_TOP POP_TOP POP_EXCEPT POP_BLOCK\n                                  JUMP_ABSOLUTE END_FINALLY COME_FROM\n                                  for_block pb_ja\n                                  else_suite COME_FROM_LOOP\n\n        ')
        self.check_reduce['call_kw'] = 'AST'
        for (i, token) in enumerate(tokens):
            opname = token.kind
            if opname == 'FORMAT_VALUE':
                rules_str = '\n                    expr              ::= formatted_value1\n                    formatted_value1  ::= expr FORMAT_VALUE\n                '
                self.add_unique_doc_rules(rules_str, customize)
            elif opname == 'FORMAT_VALUE_ATTR':
                rules_str = '\n                expr              ::= formatted_value2\n                formatted_value2  ::= expr expr FORMAT_VALUE_ATTR\n                '
                self.add_unique_doc_rules(rules_str, customize)
            elif opname == 'MAKE_FUNCTION_8':
                if 'LOAD_DICTCOMP' in self.seen_ops:
                    rule = '\n                       dict_comp ::= load_closure LOAD_DICTCOMP LOAD_STR\n                                     MAKE_FUNCTION_8 expr\n                                     GET_ITER CALL_FUNCTION_1\n                       '
                    self.addRule(rule, nop_func)
                elif 'LOAD_SETCOMP' in self.seen_ops:
                    rule = '\n                       set_comp ::= load_closure LOAD_SETCOMP LOAD_STR\n                                    MAKE_FUNCTION_8 expr\n                                    GET_ITER CALL_FUNCTION_1\n                       '
                    self.addRule(rule, nop_func)
            elif opname == 'BEFORE_ASYNC_WITH':
                rules_str = '\n                  stmt ::= async_with_stmt\n                  async_with_pre     ::= BEFORE_ASYNC_WITH GET_AWAITABLE LOAD_CONST YIELD_FROM SETUP_ASYNC_WITH\n                  async_with_post    ::= COME_FROM_ASYNC_WITH\n                                         WITH_CLEANUP_START GET_AWAITABLE LOAD_CONST YIELD_FROM\n                                         WITH_CLEANUP_FINISH END_FINALLY\n                  async_with_as_stmt ::= expr\n                               async_with_pre\n                               store\n                               suite_stmts_opt\n                               POP_BLOCK LOAD_CONST\n                               async_with_post\n                 stmt ::= async_with_as_stmt\n                 async_with_stmt ::= expr\n                               POP_TOP\n                               suite_stmts_opt\n                               POP_BLOCK LOAD_CONST\n                               async_with_post\n                 async_with_stmt ::= expr\n                               POP_TOP\n                               suite_stmts_opt\n                               async_with_post\n                '
                self.addRule(rules_str, nop_func)
            elif opname.startswith('BUILD_STRING'):
                v = token.attr
                rules_str = '\n                    expr                 ::= joined_str\n                    joined_str           ::= %sBUILD_STRING_%d\n                ' % ('expr ' * v, v)
                self.add_unique_doc_rules(rules_str, customize)
                if 'FORMAT_VALUE_ATTR' in self.seen_ops:
                    rules_str = '\n                      formatted_value_attr ::= expr expr FORMAT_VALUE_ATTR expr BUILD_STRING\n                      expr                 ::= formatted_value_attr\n                    '
                    self.add_unique_doc_rules(rules_str, customize)
            elif opname.startswith('BUILD_MAP_UNPACK_WITH_CALL'):
                v = token.attr
                rule = 'build_map_unpack_with_call ::= %s%s' % ('expr ' * v, opname)
                self.addRule(rule, nop_func)
            elif opname.startswith('BUILD_TUPLE_UNPACK_WITH_CALL'):
                v = token.attr
                rule = 'build_tuple_unpack_with_call ::= ' + 'expr1024 ' * int(v // 1024) + 'expr32 ' * int(v // 32 % 32) + 'expr ' * (v % 32) + opname
                self.addRule(rule, nop_func)
                rule = 'starred ::= %s %s' % ('expr ' * v, opname)
                self.addRule(rule, nop_func)
            elif opname == 'SETUP_ANNOTATIONS':
                rule = '\n                    stmt ::= SETUP_ANNOTATIONS\n                    stmt ::= ann_assign_init_value\n                    stmt ::= ann_assign_no_init\n\n                    ann_assign_init_value ::= expr store store_annotation\n                    ann_assign_no_init    ::= store_annotation\n                    store_annotation      ::= LOAD_NAME STORE_ANNOTATION\n                    store_annotation      ::= subscript STORE_ANNOTATION\n                 '
                self.addRule(rule, nop_func)
                self.check_reduce['assign'] = 'token'
            elif opname == 'SETUP_WITH':
                rules_str = '\n                with       ::= expr SETUP_WITH POP_TOP suite_stmts_opt COME_FROM_WITH\n                               WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n\n                # Removes POP_BLOCK LOAD_CONST from 3.6-\n                withasstmt ::= expr SETUP_WITH store suite_stmts_opt COME_FROM_WITH\n                               WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n                '
                if self.version < 3.8:
                    rules_str += '\n                    with       ::= expr SETUP_WITH POP_TOP suite_stmts_opt POP_BLOCK\n                                   LOAD_CONST\n                                   WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n                    '
                else:
                    rules_str += '\n                    with       ::= expr SETUP_WITH POP_TOP suite_stmts_opt POP_BLOCK\n                                   BEGIN_FINALLY COME_FROM_WITH\n                                   WITH_CLEANUP_START WITH_CLEANUP_FINISH\n                                   END_FINALLY\n                    '
                self.addRule(rules_str, nop_func)

    def custom_classfunc_rule(self, opname, token, customize, next_token, is_pypy):
        (args_pos, args_kw) = self.get_pos_kw(token)
        nak = (len(opname) - len('CALL_FUNCTION')) // 3
        uniq_param = args_kw + args_pos
        if frozenset(('GET_AWAITABLE', 'YIELD_FROM')).issubset(self.seen_ops):
            rule = 'async_call ::= expr ' + 'pos_arg ' * args_pos + 'kwarg ' * args_kw + 'expr ' * nak + token.kind + ' GET_AWAITABLE LOAD_CONST YIELD_FROM'
            self.add_unique_rule(rule, token.kind, uniq_param, customize)
            self.add_unique_rule('expr ::= async_call', token.kind, uniq_param, customize)
        if opname.startswith('CALL_FUNCTION_KW'):
            if is_pypy:
                super(Python36Parser, self).custom_classfunc_rule(opname, token, customize, next_token, is_pypy)
            else:
                self.addRule('expr ::= call_kw36', nop_func)
                values = 'expr ' * token.attr
                rule = 'call_kw36 ::= expr %s LOAD_CONST %s' % (values, opname)
                self.add_unique_rule(rule, token.kind, token.attr, customize)
        elif opname == 'CALL_FUNCTION_EX_KW':
            self.addRule('expr        ::= call_ex_kw4\n                            call_ex_kw4 ::= expr\n                                            expr\n                                            expr\n                                            CALL_FUNCTION_EX_KW\n                         ', nop_func)
            if 'BUILD_MAP_UNPACK_WITH_CALL' in self.seen_op_basenames:
                self.addRule('expr        ::= call_ex_kw\n                                call_ex_kw  ::= expr expr build_map_unpack_with_call\n                                                CALL_FUNCTION_EX_KW\n                             ', nop_func)
            if 'BUILD_TUPLE_UNPACK_WITH_CALL' in self.seen_op_basenames:
                self.addRule('expr        ::= call_ex_kw3\n                                call_ex_kw3 ::= expr\n                                                build_tuple_unpack_with_call\n                                                expr\n                                                CALL_FUNCTION_EX_KW\n                             ', nop_func)
                if 'BUILD_MAP_UNPACK_WITH_CALL' in self.seen_op_basenames:
                    self.addRule('expr        ::= call_ex_kw2\n                                    call_ex_kw2 ::= expr\n                                                    build_tuple_unpack_with_call\n                                                    build_map_unpack_with_call\n                                                    CALL_FUNCTION_EX_KW\n                             ', nop_func)
        elif opname == 'CALL_FUNCTION_EX':
            self.addRule('\n                         expr        ::= call_ex\n                         starred     ::= expr\n                         call_ex     ::= expr starred CALL_FUNCTION_EX\n                         ', nop_func)
            if self.version >= 3.6:
                if 'BUILD_MAP_UNPACK_WITH_CALL' in self.seen_ops:
                    self.addRule('\n                            expr        ::= call_ex_kw\n                            call_ex_kw  ::= expr expr\n                                            build_map_unpack_with_call CALL_FUNCTION_EX\n                            ', nop_func)
                if 'BUILD_TUPLE_UNPACK_WITH_CALL' in self.seen_ops:
                    self.addRule('\n                            expr        ::= call_ex_kw3\n                            call_ex_kw3 ::= expr\n                                            build_tuple_unpack_with_call\n                                            %s\n                                            CALL_FUNCTION_EX\n                            ' % 'expr ' * token.attr, nop_func)
                self.addRule('\n                            expr        ::= call_ex_kw4\n                            call_ex_kw4 ::= expr\n                                            expr\n                                            expr\n                                            CALL_FUNCTION_EX\n                            ', nop_func)
        else:
            super(Python36Parser, self).custom_classfunc_rule(opname, token, customize, next_token, is_pypy)

    def reduce_is_invalid(self, rule, ast, tokens, first, last):
        invalid = super(Python36Parser, self).reduce_is_invalid(rule, ast, tokens, first, last)
        if invalid:
            return invalid
        if rule[0] == 'assign':
            if len(tokens) >= last + 1 and tokens[last] == 'LOAD_NAME' and tokens[(last + 1)] == 'STORE_ANNOTATION' and tokens[(last - 1)].pattr == tokens[(last + 1)].pattr:
                return True
        if rule[0] == 'call_kw':
            nt = ast[0]
            while not isinstance(nt, Token):
                if nt[0] == 'call_kw':
                    return True
                nt = nt[0]

        return False


class Python36ParserSingle(Python36Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python36Parser()
    p.check_grammar()
    from uncompyle6 import PYTHON_VERSION, IS_PYPY
    if PYTHON_VERSION == 3.6:
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