# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/customize3.py
# Compiled at: 2020-04-20 22:50:15
"""Isolate Python 3 version-specific semantic actions here.
"""
from uncompyle6.semantics.consts import TABLE_DIRECT
from xdis.util import co_flags_is_async
from xdis import iscode
from uncompyle6.scanner import Code
from uncompyle6.semantics.helper import find_code_node, gen_function_parens_adjust
from uncompyle6.semantics.make_function3 import make_function3_annotate
from uncompyle6.semantics.customize35 import customize_for_version35
from uncompyle6.semantics.customize36 import customize_for_version36
from uncompyle6.semantics.customize37 import customize_for_version37
from uncompyle6.semantics.customize38 import customize_for_version38

def customize_for_version3(self, version):
    TABLE_DIRECT.update({'comp_for': (' for %c in %c', (2, 'store'), (0, 'expr')), 'if_exp_not': ('%c if not %c else %c', (2, 'expr'), (0, 'expr'), (4, 'expr')), 'except_cond2': ('%|except %c as %c:\n', (1, 'expr'), (5, 'store')), 'function_def_annotate': ('\n\n%|def %c%c\n', -1, 0), 'call_generator': ('%c%P', 0, (1, -1, ', ', 100)), 'importmultiple': ('%|import %c%c\n', 2, 3), 'import_cont': (', %c', 2), 'kwarg': ('%[0]{attr}=%c', 1), 'raise_stmt2': ('%|raise %c from %c\n', 0, 1), 'tf_tryelsestmtl3': ('%c%-%c%|else:\n%+%c', 1, 3, 5), 'store_locals': ('%|# inspect.currentframe().f_locals = __locals__\n',), 'with': ('%|with %c:\n%+%c%-', 0, 3), 'withasstmt': ('%|with %c as (%c):\n%+%c%-', 0, 2, 3)})
    assert version >= 3.0

    def tryfinallystmt(node):
        suite_stmts = node[1][0]
        if len(suite_stmts) == 1 and suite_stmts[0] == 'stmt':
            stmt = suite_stmts[0]
            try_something = stmt[0]
            if try_something == 'try_except':
                try_something.kind = 'tf_try_except'
            if try_something.kind.startswith('tryelsestmt'):
                if try_something == 'tryelsestmtl3':
                    try_something.kind = 'tf_tryelsestmtl3'
                else:
                    try_something.kind = 'tf_tryelsestmt'
        self.default(node)

    self.n_tryfinallystmt = tryfinallystmt

    def listcomp_closure3(node):
        """List comprehensions in Python 3 when handled as a closure.
        See if we can combine code.
        """
        p = self.prec
        self.prec = 27
        code_obj = node[1].attr
        assert iscode(code_obj)
        code = Code(code_obj, self.scanner, self.currentclass)
        ast = self.build_ast(code._tokens, code._customize)
        self.customize(code._customize)
        while len(ast) == 1 or ast in ('sstmt', 'return') and ast[(-1)] in ('RETURN_LAST',
                                                                            'RETURN_VALUE'):
            self.prec = 100
            ast = ast[0]

        n = ast[1]
        collections = [
         node[(-3)]]
        list_ifs = []
        if self.version == 3.0 and n != 'list_iter':
            stores = [
             ast[3]]
            assert ast[4] == 'comp_iter'
            n = ast[4]
            while n == 'comp_iter':
                if n[0] == 'comp_for':
                    n = n[0]
                    stores.append(n[2])
                    n = n[3]
                elif n[0] in ('comp_if', 'comp_if_not'):
                    n = n[0]
                    if n[0].kind == 'expr':
                        list_ifs.append(n)
                    else:
                        list_ifs.append([1])
                    n = n[2]
                else:
                    break

            self.preorder(n[1])
        else:
            assert n == 'list_iter'
            stores = []
            while n == 'list_iter':
                n = n[0]
                if n == 'list_for':
                    stores.append(n[2])
                    n = n[3]
                    if n[0] == 'list_for':
                        c = n[0][0]
                        if c == 'expr':
                            c = c[0]
                        if c == 'attribute':
                            c = c[0]
                        collections.append(c)
                elif n in ('list_if', 'list_if_not'):
                    if n[0].kind == 'expr':
                        list_ifs.append(n)
                    else:
                        list_ifs.append([1])
                    n = n[2]
                elif n == 'list_if37':
                    list_ifs.append(n)
                    n = n[(-1)]
                elif n == 'list_afor':
                    collections.append(n[0][0])
                    n = n[1]
                    stores.append(n[1][0])
                    n = n[3]

            assert n == 'lc_body', ast
            self.preorder(n[0])
        n_colls = len(collections)
        for (i, store) in enumerate(stores):
            if i >= n_colls:
                break
            if collections[i] == 'LOAD_DEREF' and co_flags_is_async(code_obj.co_flags):
                self.write(' async')
            self.write(' for ')
            self.preorder(store)
            self.write(' in ')
            self.preorder(collections[i])
            if i < len(list_ifs):
                self.preorder(list_ifs[i])

        self.prec = p

    self.listcomp_closure3 = listcomp_closure3

    def n_classdef3(node):
        """Handle "classdef" nonterminal for 3.0 >= version 3.0 <= 3.5
        """
        assert 3.0 <= self.version <= 3.5
        cclass = self.currentclass
        subclass_info = None
        if node == 'classdefdeco2':
            if self.version <= 3.3:
                class_name = node[2][0].attr
            else:
                class_name = node[1][2].attr
            build_class = node
        else:
            build_class = node[0]
            class_name = node[1][0].attr
            build_class = node[0]
        assert 'mkfunc' == build_class[1]
        mkfunc = build_class[1]
        if mkfunc[0] in ('kwargs', 'no_kwargs'):
            if 3.0 <= self.version <= 3.2:
                for n in mkfunc:
                    if hasattr(n, 'attr') and iscode(n.attr):
                        subclass_code = n.attr
                        break
                    elif n == 'expr':
                        subclass_code = n[0].attr

            for n in mkfunc:
                if hasattr(n, 'attr') and iscode(n.attr):
                    subclass_code = n.attr
                    break

            if node == 'classdefdeco2':
                subclass_info = node
            else:
                subclass_info = node[0]
        elif build_class[1][0] == 'load_closure':
            load_closure = build_class[1]
            if hasattr(load_closure[(-3)], 'attr'):
                subclass_code = find_code_node(load_closure, -3).attr
            elif hasattr(load_closure[(-2)], 'attr'):
                subclass_code = find_code_node(load_closure, -2).attr
            else:
                raise 'Internal Error n_classdef: cannot find class body'
            if hasattr(build_class[3], '__len__'):
                if not subclass_info:
                    subclass_info = build_class[3]
            elif hasattr(build_class[2], '__len__'):
                subclass_info = build_class[2]
            else:
                raise 'Internal Error n_classdef: cannot superclass name'
        elif not subclass_info:
            if mkfunc[0] in ('no_kwargs', 'kwargs'):
                subclass_code = mkfunc[1].attr
            else:
                subclass_code = mkfunc[0].attr
            if node == 'classdefdeco2':
                subclass_info = node
            else:
                subclass_info = node[0]
        if node == 'classdefdeco2':
            self.write('\n')
        else:
            self.write('\n\n')
        self.currentclass = str(class_name)
        self.write(self.indent, 'class ', self.currentclass)
        self.print_super_classes3(subclass_info)
        self.println(':')
        self.indent_more()
        self.build_class(subclass_code)
        self.indent_less()
        self.currentclass = cclass
        if len(self.param_stack) > 1:
            self.write('\n\n')
        else:
            self.write('\n\n\n')
        self.prune()
        return

    self.n_classdef3 = n_classdef3
    if version == 3.0:
        TABLE_DIRECT.update({'ifstmt30': ('%|if %c:\n%+%c%-', (0, 'testfalse_then'), (1, '_ifstmts_jump30')), 'ifnotstmt30': ('%|if not %c:\n%+%c%-', (0, 'testtrue_then'), (1, '_ifstmts_jump30')), 'try_except30': ('%|try:\n%+%c%-%c\n\n', (1, 'suite_stmts_opt'), (4, 'except_handler'))})

        def n_comp_iter(node):
            if node[0] == 'expr':
                n = node[0][0]
                if n == 'LOAD_FAST' and n.pattr[0:2] == '_[':
                    self.prune()
            self.default(node)

        self.n_comp_iter = n_comp_iter
    elif version == 3.3:

        def n_yield_from(node):
            assert node[0] == 'expr'
            if node[0][0] == 'get_iter':
                template = (
                 'yield from %c', (0, 'expr'))
                self.template_engine(template, node[0][0])
            else:
                template = (
                 'yield from %c', (0, 'attribute'))
                self.template_engine(template, node[0][0][0])
            self.prune()

        self.n_yield_from = n_yield_from
    if 3.2 <= version <= 3.4:

        def n_call(node):
            mapping = self._get_mapping(node)
            key = node
            for i in mapping[1:]:
                key = key[i]

            if key.kind.startswith('CALL_FUNCTION_VAR_KW'):
                pass
            elif key.kind.startswith('CALL_FUNCTION_VAR'):
                argc = node[(-1)].attr
                nargs = argc & 255
                kwargs = argc >> 8 & 255
                if kwargs != 0:
                    if nargs == 0:
                        template = (
                         '%c(*%c, %C)', 0, -2, (1, kwargs + 1, ', '))
                    else:
                        template = (
                         '%c(%C, *%c, %C)', 0, (1, nargs + 1, ', '), -2, (-2 - kwargs, -2, ', '))
                    self.template_engine(template, node)
                    self.prune()
            else:
                gen_function_parens_adjust(key, node)
            self.default(node)

        self.n_call = n_call
    elif version < 3.2:

        def n_call(node):
            mapping = self._get_mapping(node)
            key = node
            for i in mapping[1:]:
                key = key[i]

            gen_function_parens_adjust(key, node)
            self.default(node)

        self.n_call = n_call

    def n_mkfunc_annotate(node):
        if node[(-2)] == 'EXTENDED_ARG':
            i = -1
        else:
            i = 0
        if self.version <= 3.2:
            code = node[(-2 + i)]
        elif self.version >= 3.3 or node[(-2)] == 'kwargs':
            code = node[(-3 + i)]
        elif node[(-3)] == 'expr':
            code = node[(-3)][0]
        else:
            code = node[(-3)]
        self.indent_more()
        for annotate_last in range(len(node) - 1, -1, -1):
            if node[annotate_last] == 'annotate_tuple':
                break

        if self.f.getvalue()[-4:] == 'def ':
            self.write(code.attr.co_name)
        make_function3_annotate(self, node, is_lambda=False, code_node=code, annotate_last=annotate_last)
        if len(self.param_stack) > 1:
            self.write('\n\n')
        else:
            self.write('\n\n\n')
        self.indent_less()
        self.prune()

    self.n_mkfunc_annotate = n_mkfunc_annotate
    TABLE_DIRECT.update({'tryelsestmtl3': ('%|try:\n%+%c%-%c%|else:\n%+%c%-', (1, 'suite_stmts_opt'), 3, (5, 'else_suitel')), 'LOAD_CLASSDEREF': ('%{pattr}',)})
    if version >= 3.4:
        TABLE_DIRECT.update({'LOAD_CLASSDEREF': ('%{pattr}',), 'yield_from': ('yield from %c', (0, 'expr'))})
        if version >= 3.5:
            customize_for_version35(self, version)
            if version >= 3.6:
                customize_for_version36(self, version)
                if version >= 3.7:
                    customize_for_version37(self, version)
                    if version >= 3.8:
                        customize_for_version38(self, version)
    return