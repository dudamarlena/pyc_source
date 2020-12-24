# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/make_function36.py
# Compiled at: 2020-04-27 23:06:35
"""
All the crazy things we have to do to handle Python functions in 3.6 and above.
The saga of changes before 3.6 is in other files.
"""
from xdis import iscode, code_has_star_arg, code_has_star_star_arg
from xdis.util import CO_GENERATOR, CO_ASYNC_GENERATOR
from uncompyle6.scanner import Code
from uncompyle6.parsers.treenode import SyntaxTree
from uncompyle6.semantics.parser_error import ParserError
from uncompyle6.parser import ParserError as ParserError2
from uncompyle6 import PYTHON3
from uncompyle6.semantics.helper import print_docstring, find_all_globals, find_globals_and_nonlocals, find_none, zip_longest
from uncompyle6.show import maybe_show_tree_param_default

def make_function36(self, node, is_lambda, nested=1, code_node=None):
    """Dump function definition, doc string, and function body in
      Python version 3.6 and above.
    """

    def build_param(ast, name, default, annotation=None):
        """build parameters:
            - handle defaults
            - handle format tuple parameters
        """
        value = default
        maybe_show_tree_param_default(self.showast, name, value)
        if annotation:
            result = '%s: %s=%s' % (name, annotation, value)
        else:
            result = '%s=%s' % (name, value)
        if result[-2:] == '= ':
            result += 'None'
        return result

    assert node[(-1)].kind.startswith('MAKE_')
    lambda_index = -3
    args_node = node[(-1)]
    annotate_dict = {}
    args_attr = args_node.attr
    if len(args_attr) == 3:
        (pos_args, kw_args, annotate_argc) = args_attr
    else:
        (pos_args, kw_args, annotate_argc, closure) = args_attr
    if node[(-2)] != 'docstring':
        i = -4
    else:
        i = -5
    kw_pairs = 0
    if annotate_argc:
        annotate_node = node[i]
        if annotate_node == 'expr':
            annotate_node = annotate_node[0]
            annotate_name_node = annotate_node[(-1)]
            if annotate_node == 'dict':
                if annotate_name_node.kind.startswith('BUILD_CONST_KEY_MAP'):
                    types = [ self.traverse(n, indent='') for n in annotate_node[:-2] ]
                    names = annotate_node[(-2)].attr
                    l = len(types)
                    assert l == len(names)
                    for i in range(l):
                        annotate_dict[names[i]] = types[i]

            i -= 1
        if closure:
            i -= 1
        if kw_args:
            kw_node = node[pos_args]
            if kw_node == 'expr':
                kw_node = kw_node[0]
            if kw_node == 'dict':
                kw_pairs = kw_node[(-1)].attr
        defparams = []
        (default, kw_args, annotate_argc) = args_node.attr[0:3]
        if default:
            expr_node = node[0]
            if node[0] == 'pos_arg':
                expr_node = expr_node[0]
            assert expr_node == 'expr', 'expecting mkfunc default node to be an expr'
            if expr_node[0] == 'LOAD_CONST' and isinstance(expr_node[0].attr, tuple):
                defparams = [ repr(a) for a in expr_node[0].attr ]
            elif expr_node[0] in frozenset(('list', 'tuple', 'dict', 'set')):
                defparams = [ self.traverse(n, indent='') for n in expr_node[0][:-1] ]
        else:
            defparams = []
        assert lambda_index and is_lambda and iscode(node[lambda_index].attr) and node[lambda_index].kind == 'LOAD_LAMBDA'
        code = node[lambda_index].attr
    else:
        code = code_node.attr
    assert iscode(code)
    scanner_code = Code(code, self.scanner, self.currentclass)
    argc = code.co_argcount
    kwonlyargcount = code.co_kwonlyargcount
    paramnames = list(scanner_code.co_varnames[:argc])
    kwargs = list(scanner_code.co_varnames[argc:argc + kwonlyargcount])
    paramnames.reverse()
    defparams.reverse()
    try:
        ast = self.build_ast(scanner_code._tokens, scanner_code._customize, is_lambda=is_lambda, noneInNames='None' in code.co_names)
    except ParserError, p:
        self.write(str(p))
        if not self.tolerate_errors:
            self.ERROR = p
        return

    i = len(paramnames) - len(defparams)
    params = []
    if defparams:
        for (i, defparam) in enumerate(defparams):
            params.append(build_param(ast, paramnames[i], defparam, annotate_dict.get(paramnames[i])))

        for param in paramnames[i + 1:]:
            if param in annotate_dict:
                params.append('%s: %s' % (param, annotate_dict[param]))
            else:
                params.append(param)

    else:
        for param in paramnames:
            if param in annotate_dict:
                params.append('%s: %s' % (param, annotate_dict[param]))
            else:
                params.append(param)

        params.reverse()
        if code_has_star_arg(code):
            star_arg = code.co_varnames[(argc + kwonlyargcount)]
            if star_arg in annotate_dict:
                params.append('*%s: %s' % (star_arg, annotate_dict[star_arg]))
            else:
                params.append('*%s' % star_arg)
            argc += 1
        if is_lambda:
            self.write('lambda ', (', ').join(params))
            if len(ast) > 1:
                if self.traverse(ast[(-1)]) == 'None':
                    if self.traverse(ast[(-2)]).strip().startswith('yield'):
                        del ast[-1]
                        ast_expr = ast[(-1)]
                        while ast_expr.kind != 'expr':
                            ast_expr = ast_expr[0]

                        ast[-1] = ast_expr
                else:
                    self.write('(', (', ').join(params))
                ends_in_comma = False
                if kwonlyargcount > 0:
                    if 4 & code.co_flags or argc > 0:
                        self.write(', *, ')
                    else:
                        self.write('*, ')
                    ends_in_comma = True
                elif argc > 0:
                    self.write(', ')
                    ends_in_comma = True
                ann_dict = kw_dict = default_tup = None
                fn_bits = node[(-1)].attr
                if node[(-2)] == 'docstring':
                    index = -5
                else:
                    index = -4
                if fn_bits[(-1)]:
                    index -= 1
                if fn_bits[(-2)]:
                    ann_dict = node[index]
                    index -= 1
                if fn_bits[(-3)]:
                    kw_dict = node[index]
                    index -= 1
                if fn_bits[(-4)]:
                    default_tup = node[index]
                if kw_dict == 'expr':
                    kw_dict = kw_dict[0]
                kw_args = [None] * kwonlyargcount
                assert kw_dict and kw_dict == 'dict'
                defaults = [ self.traverse(n, indent='') for n in kw_dict[:-2] ]
                names = eval(self.traverse(kw_dict[(-2)]))
                assert len(defaults) == len(names)
                sep = ''
                for (i, n) in enumerate(names):
                    idx = kwargs.index(n)
                    if annotate_dict and n in annotate_dict:
                        t = '%s: %s=%s' % (n, annotate_dict[n], defaults[i])
                    else:
                        t = '%s=%s' % (n, defaults[i])
                    kw_args[idx] = t

            other_kw = [ c == None for c in kw_args ]
            for (i, flag) in enumerate(other_kw):
                if flag:
                    n = kwargs[i]
                    if n in annotate_dict:
                        kw_args[i] = '%s: %s' % (n, annotate_dict[n])
                    else:
                        kw_args[i] = '%s' % n

            self.write((', ').join(kw_args))
            ends_in_comma = False
        elif argc == 0:
            ends_in_comma = True
        if code_has_star_star_arg(code):
            if not ends_in_comma:
                self.write(', ')
            star_star_arg = code.co_varnames[(argc + kwonlyargcount)]
            if annotate_dict and star_star_arg in annotate_dict:
                self.write('**%s: %s' % (star_star_arg, annotate_dict[star_star_arg]))
            else:
                self.write('**%s' % star_star_arg)
        if is_lambda:
            self.write(': ')
        else:
            self.write(')')
            if annotate_dict and 'return' in annotate_dict:
                self.write(' -> %s' % annotate_dict['return'])
            self.println(':')
    if node[(-2)] == 'docstring' and not is_lambda:
        self.println(self.traverse(node[(-2)]))
    assert ast == 'stmts'
    all_globals = find_all_globals(ast, set())
    (globals, nonlocals) = find_globals_and_nonlocals(ast, set(), set(), code, self.version)
    for g in sorted(all_globals & self.mod_globs | globals):
        self.println(self.indent, 'global ', g)

    for nl in sorted(nonlocals):
        self.println(self.indent, 'nonlocal ', nl)

    self.mod_globs -= all_globals
    has_none = 'None' in code.co_names
    rn = has_none and not find_none(ast)
    self.gen_source(ast, code.co_name, scanner_code._customize, is_lambda=is_lambda, returnNone=rn)
    if not is_lambda and code.co_flags & (CO_GENERATOR | CO_ASYNC_GENERATOR):
        need_bogus_yield = True
        for token in scanner_code._tokens:
            if token == 'YIELD_VALUE':
                need_bogus_yield = False
                break

        if need_bogus_yield:
            self.template_engine(('%|if False:\n%+%|yield None%-', ), node)
    scanner_code._tokens = None
    scanner_code._customize = None
    return