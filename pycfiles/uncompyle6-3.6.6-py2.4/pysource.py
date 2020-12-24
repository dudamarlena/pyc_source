# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/pysource.py
# Compiled at: 2020-04-20 23:09:13
"""Creates Python source code from an uncompyle6 parse tree.

The terminal symbols are CPython bytecode instructions. (See the
python documentation under module "dis" for a list of instructions
and what they mean).

Upper levels of the grammar is a more-or-less conventional grammar for
Python.
"""
import sys
IS_PYPY = '__pypy__' in sys.builtin_module_names
PYTHON3 = sys.version_info >= (3, 0)
from xdis import iscode
from xdis.util import COMPILER_FLAG_BIT
from uncompyle6.parser import get_python_parser
from uncompyle6.parsers.treenode import SyntaxTree
from spark_parser import GenericASTTraversal, DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.scanner import Code, get_scanner
import uncompyle6.parser as python_parser
from uncompyle6.semantics.make_function2 import make_function2
from uncompyle6.semantics.make_function3 import make_function3
from uncompyle6.semantics.make_function36 import make_function36
from uncompyle6.semantics.parser_error import ParserError
from uncompyle6.semantics.check_ast import checker
from uncompyle6.semantics.customize import customize_for_version
from uncompyle6.semantics.helper import print_docstring, find_code_node, find_globals_and_nonlocals, flatten_list
from uncompyle6.scanners.tok import Token
from uncompyle6.semantics.transform import is_docstring, TreeTransform
from uncompyle6.semantics.consts import LINE_LENGTH, RETURN_LOCALS, NONE, RETURN_NONE, PASS, ASSIGN_DOC_STRING, NAME_MODULE, TAB, INDENT_PER_LEVEL, TABLE_R, MAP_DIRECT, MAP, PRECEDENCE, ASSIGN_TUPLE_PARAM, escape, minint
from uncompyle6.show import maybe_show_tree
from uncompyle6.util import better_repr
if PYTHON3:
    from io import StringIO
else:
    from StringIO import StringIO

class SourceWalkerError(Exception):
    __module__ = __name__

    def __init__(self, errmsg):
        self.errmsg = errmsg

    def __str__(self):
        return self.errmsg


class SourceWalker(GenericASTTraversal, object):
    __module__ = __name__
    stacked_params = ('f', 'indent', 'is_lambda', '_globals')

    def __init__(self, version, out, scanner, showast=False, debug_parser=PARSER_DEFAULT_DEBUG, compile_mode='exec', is_pypy=IS_PYPY, linestarts={}, tolerate_errors=False):
        """`version' is the Python version (a float) of the Python dialect
        of both the syntax tree and language we should produce.

        `out' is IO-like file pointer to where the output should go. It
        whould have a getvalue() method.

        `scanner' is a method to call when we need to scan tokens. Sometimes
        in producing output we will run across further tokens that need
        to be scaned.

        If `showast' is True, we print the syntax tree.

        `compile_mode' is is either 'exec' or 'single'. It isthe compile
        mode that was used to create the Syntax Tree and specifies a
        gramar variant within a Python version to use.

        `is_pypy' should be True if the Syntax Tree was generated for PyPy.

        `linestarts' is a dictionary of line number to bytecode offset. This
        can sometimes assist in determinte which kind of source-code construct
        to use when there is ambiguity.

        """
        GenericASTTraversal.__init__(self, ast=None)
        self.scanner = scanner
        params = {'f': out, 'indent': ''}
        self.version = version
        self.p = get_python_parser(version, debug_parser=dict(debug_parser), compile_mode=compile_mode, is_pypy=is_pypy)
        self.treeTransform = TreeTransform(version=version, show_ast=showast, is_pypy=is_pypy)
        self.debug_parser = dict(debug_parser)
        self.showast = showast
        self.params = params
        self.param_stack = []
        self.ERROR = None
        self.prec = 100
        self.return_none = False
        self.mod_globs = set()
        self.currentclass = None
        self.classes = []
        self.pending_newlines = 0
        self.linestarts = linestarts
        self.line_number = 1
        self.ast_errors = []
        self.insts = scanner.insts
        self.offset2inst_index = scanner.offset2inst_index
        self.FUTURE_UNICODE_LITERALS = False
        self.tolerate_errors = tolerate_errors
        self.in_format_string = None
        self.hide_internal = True
        self.name = None
        self.version = version
        self.is_pypy = is_pypy
        customize_for_version(self, is_pypy, version)
        return

    def maybe_show_tree(self, ast):
        if self.showast and self.treeTransform.showast:
            self.println('\n---- end before transform\n---- begin after transform\n' + '    ')
        if isinstance(self.showast, dict) and self.showast.get:
            maybe_show_tree(self, ast)

    def str_with_template(self, ast):
        stream = sys.stdout
        stream.write(self.str_with_template1(ast, '', None))
        stream.write('\n')
        return

    def str_with_template1(self, ast, indent, sibNum=None):
        rv = str(ast.kind)
        if sibNum is not None:
            rv = '%2d. %s' % (sibNum, rv)
        enumerate_children = False
        if len(ast) > 1:
            rv += ' (%d)' % len(ast)
            enumerate_children = True
        mapping = self._get_mapping(ast)
        table = mapping[0]
        key = ast
        for i in mapping[1:]:
            key = key[i]

        if ast.transformed_by is not None:
            if ast.transformed_by is True:
                rv += ' transformed'
            else:
                rv += ' transformed by %s' % ast.transformed_by
        if key.kind in table:
            rv += ': %s' % str(table[key.kind])
        rv = indent + rv
        indent += '    '
        i = 0
        for node in ast:
            if hasattr(node, '__repr1__'):
                if enumerate_children:
                    child = self.str_with_template1(node, indent, i)
                else:
                    child = self.str_with_template1(node, indent, None)
            else:
                inst = node.format(line_prefix='L.')
                if inst.startswith('\n'):
                    inst = inst[1:]
                if enumerate_children:
                    child = indent + '%2d. %s' % (i, inst)
                else:
                    child = indent + inst
            rv += '\n' + child
            i += 1

        return rv

    def indent_if_source_nl(self, line_number, indent):
        if line_number != self.line_number:
            self.write('\n' + self.indent + INDENT_PER_LEVEL[:-1])
        return self.line_number

    f = property(lambda s: s.params['f'], lambda s, x: s.params.__setitem__('f', x), lambda s: s.params.__delitem__('f'), None)
    indent = property(lambda s: s.params['indent'], lambda s, x: s.params.__setitem__('indent', x), lambda s: s.params.__delitem__('indent'), None)
    is_lambda = property(lambda s: s.params['is_lambda'], lambda s, x: s.params.__setitem__('is_lambda', x), lambda s: s.params.__delitem__('is_lambda'), None)
    _globals = property(lambda s: s.params['_globals'], lambda s, x: s.params.__setitem__('_globals', x), lambda s: s.params.__delitem__('_globals'), None)

    def set_pos_info(self, node):
        if hasattr(node, 'linestart') and node.linestart:
            self.line_number = node.linestart

    def preorder(self, node=None):
        super(SourceWalker, self).preorder(node)
        self.set_pos_info(node)

    def indent_more(self, indent=TAB):
        self.indent += indent

    def indent_less(self, indent=TAB):
        self.indent = self.indent[:-len(indent)]

    def traverse(self, node, indent=None, is_lambda=False):
        self.param_stack.append(self.params)
        if indent is None:
            indent = self.indent
        p = self.pending_newlines
        self.pending_newlines = 0
        self.params = {'_globals': {}, '_nonlocals': {}, 'f': StringIO(), 'indent': indent, 'is_lambda': is_lambda}
        self.preorder(node)
        self.f.write('\n' * self.pending_newlines)
        result = self.f.getvalue()
        self.params = self.param_stack.pop()
        self.pending_newlines = p
        return result

    def write(self, *data):
        if len(data) == 0 or len(data) == 1 and data[0] == '':
            return
        if not PYTHON3:
            out = ('').join((unicode(j) for j in data))
        else:
            out = ('').join((str(j) for j in data))
        n = 0
        for i in out:
            if i == '\n':
                n += 1
                if n == len(out):
                    self.pending_newlines = max(self.pending_newlines, n)
                    return
            elif n:
                self.pending_newlines = max(self.pending_newlines, n)
                out = out[n:]
                break
            else:
                break

        if self.pending_newlines > 0:
            self.f.write('\n' * self.pending_newlines)
            self.pending_newlines = 0
        for i in out[::-1]:
            if i == '\n':
                self.pending_newlines += 1
            else:
                break

        if self.pending_newlines:
            out = out[:-self.pending_newlines]
        if isinstance(out, str) and not (PYTHON3 or self.FUTURE_UNICODE_LITERALS):
            out = unicode(out, 'utf-8')
        self.f.write(out)

    def println(self, *data):
        if data and not (len(data) == 1 and data[0] == ''):
            self.write(*data)
        self.pending_newlines = max(self.pending_newlines, 1)

    def is_return_none(self, node):
        ret = node[0] == 'ret_expr' and node[0][0] == 'expr' and node[0][0][0] == 'LOAD_CONST' and node[0][0][0].pattr is None
        if self.version <= 2.6:
            return ret
        else:
            return ret or node == SyntaxTree('return', [SyntaxTree('ret_expr', [NONE]), Token('RETURN_VALUE')])
        return

    def n_return_lambda(self, node):
        if 1 <= len(node) <= 2:
            self.preorder(node[0])
            self.write(' # Avoid dead code: ')
            self.prune()
        else:
            assert len(node) == 3 and node[2] in ('RETURN_VALUE_LAMBDA', 'LAMBDA_MARKER')
            self.preorder(node[0])
            self.prune()

    def n_return(self, node):
        if self.params['is_lambda']:
            self.preorder(node[0])
            self.prune()
        else:
            self.write(self.indent, 'return')
            if self.return_none or not self.is_return_none(node):
                self.write(' ')
                self.preorder(node[0])
            self.println()
            self.prune()

    def n_return_if_stmt(self, node):
        if self.params['is_lambda']:
            self.write(' return ')
            self.preorder(node[0])
            self.prune()
        else:
            self.write(self.indent, 'return')
            if self.return_none or not self.is_return_none(node):
                self.write(' ')
                self.preorder(node[0])
            self.println()
            self.prune()

    def n_yield(self, node):
        if node != SyntaxTree('yield', [NONE, Token('YIELD_VALUE')]):
            self.template_engine(('yield %c', 0), node)
        elif self.version <= 2.4:
            self.write('yield None')
        else:
            self.write('yield')
        self.prune()

    def n_build_slice3(self, node):
        p = self.prec
        self.prec = 100
        if not node[0].isNone():
            self.preorder(node[0])
        self.write(':')
        if not node[1].isNone():
            self.preorder(node[1])
        self.write(':')
        if not node[2].isNone():
            self.preorder(node[2])
        self.prec = p
        self.prune()

    def n_build_slice2(self, node):
        p = self.prec
        self.prec = 100
        if not node[0].isNone():
            self.preorder(node[0])
        self.write(':')
        if not node[1].isNone():
            self.preorder(node[1])
        self.prec = p
        self.prune()

    def n_expr(self, node):
        first_child = node[0]
        if first_child == '_mklambda' and self.in_format_string:
            p = -2
        else:
            p = self.prec
        if first_child.kind.startswith('bin_op'):
            n = node[0][(-1)][0]
        else:
            n = node[0]
        self.prec = PRECEDENCE.get(n.kind, -2)
        if n == 'LOAD_CONST' and repr(n.pattr)[0] == '-':
            self.prec = 6
        if p < self.prec:
            self.write('(')
            self.preorder(node[0])
            self.write(')')
        else:
            self.preorder(node[0])
        self.prec = p
        self.prune()

    def n_ret_expr(self, node):
        if len(node) == 1 and node[0] == 'expr':
            self.prec = PRECEDENCE['yield'] - 1
            self.n_expr(node[0])
            p = self.prec
        else:
            self.n_expr(node)

    n_ret_expr_or_cond = n_expr

    def n_bin_op(self, node):
        """bin_op (formerly "binary_expr") is the Python AST BinOp"""
        self.preorder(node[0])
        self.write(' ')
        self.preorder(node[(-1)])
        self.write(' ')
        self.prec -= 1
        self.preorder(node[1])
        self.prec += 1
        self.prune()

    def n_str(self, node):
        self.write(node[0].pattr)
        self.prune()

    def pp_tuple(self, tup):
        """Pretty print a tuple"""
        last_line = self.f.getvalue().split('\n')[(-1)]
        l = len(last_line) + 1
        indent = ' ' * l
        self.write('(')
        sep = ''
        for item in tup:
            self.write(sep)
            l += len(sep)
            s = better_repr(item, self.version)
            l += len(s)
            self.write(s)
            sep = ','
            if l > LINE_LENGTH:
                l = 0
                sep += '\n' + indent
            else:
                sep += ' '

        if len(tup) == 1:
            self.write(', ')
        self.write(')')

    def n_LOAD_CONST(self, node):
        attr = node.attr
        data = node.pattr
        datatype = type(data)
        if isinstance(data, float):
            self.write(better_repr(data, self.version))
        elif isinstance(data, complex):
            self.write(better_repr(data, self.version))
        elif isinstance(datatype, int) and data == minint:
            self.write(hex(data))
        elif datatype is type(Ellipsis):
            self.write('...')
        elif attr is None:
            self.write('None')
        elif isinstance(data, tuple):
            self.pp_tuple(data)
        elif isinstance(attr, bool):
            self.write(repr(attr))
        elif self.FUTURE_UNICODE_LITERALS:
            if not PYTHON3 and isinstance(data, unicode):
                try:
                    data = str(data)
                except UnicodeEncodeError:
                    pass
                else:
                    self.write(repr(data))
            elif isinstance(data, str):
                self.write('b' + repr(data))
            else:
                self.write(repr(data))
        else:
            if not PYTHON3:
                try:
                    repr(data).encode('ascii')
                except UnicodeEncodeError:
                    self.write('u')

            self.write(repr(data))
        self.prune()
        return

    def n_delete_subscript(self, node):
        if node[(-2)][0] == 'build_list' and node[(-2)][0][(-1)].kind.startswith('BUILD_TUPLE'):
            if node[(-2)][0][(-1)] != 'BUILD_TUPLE_0':
                node[(-2)][0].kind = 'build_tuple2'
        self.default(node)

    n_store_subscript = n_subscript = n_delete_subscript

    def n_exec_stmt(self, node):
        """
        exec_stmt ::= expr exprlist DUP_TOP EXEC_STMT
        exec_stmt ::= expr exprlist EXEC_STMT
        """
        self.write(self.indent, 'exec ')
        self.preorder(node[0])
        if not node[1][0].isNone():
            sep = ' in '
            for subnode in node[1]:
                self.write(sep)
                sep = ', '
                self.preorder(subnode)

        self.println()
        self.prune()

    def n_ifelsestmtr(self, node):
        if node[2] == 'COME_FROM':
            return_stmts_node = node[3]
            node.kind = 'ifelsestmtr2'
        else:
            return_stmts_node = node[2]
        if len(return_stmts_node) != 2:
            self.default(node)
        if not (return_stmts_node[0][0][0] == 'ifstmt' and return_stmts_node[0][0][0][1][0] == 'return_if_stmts') and not (return_stmts_node[0][(-1)][0] == 'ifstmt' and return_stmts_node[0][(-1)][0][1][0] == 'return_if_stmts'):
            self.default(node)
            return
        self.write(self.indent, 'if ')
        self.preorder(node[0])
        self.println(':')
        self.indent_more()
        self.preorder(node[1])
        self.indent_less()
        if_ret_at_end = False
        if len(return_stmts_node[0]) >= 3:
            if return_stmts_node[0][(-1)][0] == 'ifstmt' and return_stmts_node[0][(-1)][0][1][0] == 'return_if_stmts':
                if_ret_at_end = True
        past_else = False
        prev_stmt_is_if_ret = True
        for n in return_stmts_node[0]:
            if n[0] == 'ifstmt' and n[0][1][0] == 'return_if_stmts':
                if prev_stmt_is_if_ret:
                    n[0].kind = 'elifstmt'
                prev_stmt_is_if_ret = True
            else:
                prev_stmt_is_if_ret = False
                if not past_else and not if_ret_at_end:
                    self.println(self.indent, 'else:')
                    self.indent_more()
                    past_else = True
            self.preorder(n)

        if not past_else or if_ret_at_end:
            self.println(self.indent, 'else:')
            self.indent_more()
        self.preorder(return_stmts_node[1])
        self.indent_less()
        self.prune()

    n_ifelsestmtr2 = n_ifelsestmtr

    def n_elifelsestmtr(self, node):
        if node[2] == 'COME_FROM':
            return_stmts_node = node[3]
            node.kind = 'elifelsestmtr2'
        else:
            return_stmts_node = node[2]
        if len(return_stmts_node) != 2:
            self.default(node)
        for n in return_stmts_node[0]:
            if not (n[0] == 'ifstmt' and n[0][1][0] == 'return_if_stmts'):
                self.default(node)
                return

        self.write(self.indent, 'elif ')
        self.preorder(node[0])
        self.println(':')
        self.indent_more()
        self.preorder(node[1])
        self.indent_less()
        for n in return_stmts_node[0]:
            n[0].kind = 'elifstmt'
            self.preorder(n)

        self.println(self.indent, 'else:')
        self.indent_more()
        self.preorder(return_stmts_node[1])
        self.indent_less()
        self.prune()

    def n_alias(self, node):
        if self.version <= 2.1:
            if len(node) == 2:
                store = node[1]
                assert store == 'store'
                if store[0].pattr == node[0].pattr:
                    self.write('import %s\n' % node[0].pattr)
                else:
                    self.write('import %s as %s\n' % (node[0].pattr, store[0].pattr))
            self.prune()
        store_node = node[(-1)][(-1)]
        assert store_node.kind.startswith('STORE_')
        iname = node[0].pattr
        sname = store_node.pattr
        if iname and iname == sname or iname.startswith(sname + '.'):
            self.write(iname)
        else:
            self.write(iname, ' as ', sname)
        self.prune()

    n_alias37 = n_alias

    def n_import_from(self, node):
        relative_path_index = 0
        if self.version >= 2.5:
            if node[relative_path_index].pattr > 0:
                node[2].pattr = '.' * node[relative_path_index].pattr + node[2].pattr
            if self.version > 2.7:
                if isinstance(node[1].pattr, tuple):
                    imports = node[1].pattr
                    for pattr in imports:
                        node[1].pattr = pattr
                        self.default(node)

                    return
        self.default(node)

    n_import_from_star = n_import_from

    def n_mkfunc(self, node):
        code_node = find_code_node(node, -2)
        code = code_node.attr
        self.write(code.co_name)
        self.indent_more()
        self.make_function(node, is_lambda=False, code_node=code_node)
        if len(self.param_stack) > 1:
            self.write('\n\n')
        else:
            self.write('\n\n\n')
        self.indent_less()
        self.prune()

    def make_function(self, node, is_lambda, nested=1, code_node=None, annotate=None):
        if self.version <= 2.7:
            make_function2(self, node, is_lambda, nested, code_node)
        elif 3.0 <= self.version <= 3.5:
            make_function3(self, node, is_lambda, nested, code_node)
        elif self.version >= 3.6:
            make_function36(self, node, is_lambda, nested, code_node)

    def n_docstring(self, node):
        indent = self.indent
        doc_node = node[0]
        if doc_node.attr:
            docstring = doc_node.attr
        else:
            docstring = node[0].pattr
        quote = '"""'
        if docstring.find(quote) >= 0:
            if docstring.find("'''") == -1:
                quote = "'''"
        self.write(indent)
        docstring = repr(docstring.expandtabs())[1:-1]
        for (orig, replace) in (('\\\\', '\t'), ('\\r\\n', '\n'), ('\\n', '\n'), ('\\r', '\n'), ('\\"', '"'), ("\\'", "'")):
            docstring = docstring.replace(orig, replace)

        if '\t' in docstring and '\\' not in docstring and len(docstring) >= 2 and docstring[(-1)] != '\t' and (docstring[(-1)] != '"' or docstring[(-2)] == '\t'):
            self.write('r')
            docstring = docstring.replace('\t', '\\')
        else:
            quote1 = quote[(-1)]
            if len(docstring) and docstring[(-1)] == quote1:
                docstring = docstring[:-1] + '\\' + quote1
            if quote == '"""':
                replace_str = '\\"""'
            else:
                assert quote == "'''"
                replace_str = "\\'''"
            docstring = docstring.replace(quote, replace_str)
            docstring = docstring.replace('\t', '\\\\')
        lines = docstring.split('\n')
        self.write(quote)
        if len(lines) == 0:
            self.println(quote)
        elif len(lines) == 1:
            self.println(lines[0], quote)
        else:
            self.println(lines[0])
            for line in lines[1:-1]:
                if line:
                    self.println(line)
                else:
                    self.println('\n\n')

            self.println(lines[(-1)], quote)
        self.prune()

    def n_mklambda(self, node):
        self.make_function(node, is_lambda=True, code_node=node[(-2)])
        self.prune()

    def n_list_comp(self, node):
        """List comprehensions"""
        p = self.prec
        self.prec = 100
        if self.version >= 2.7:
            if self.is_pypy:
                self.n_list_comp_pypy27(node)
                return
            n = node[(-1)]
        elif node[(-1)] == 'del_stmt':
            if node[(-2)] == 'JUMP_BACK':
                n = node[(-3)]
            else:
                n = node[(-2)]
        assert n == 'list_iter'
        while n == 'list_iter':
            n = n[0]
            if n == 'list_for':
                n = n[3]
            elif n == 'list_if':
                n = n[2]
            elif n == 'list_if_not':
                n = n[2]

        assert n == 'lc_body'
        self.write('[ ')
        if self.version >= 2.7:
            expr = n[0]
            list_iter = node[(-1)]
        else:
            expr = n[1]
            if node[(-2)] == 'JUMP_BACK':
                list_iter = node[(-3)]
            else:
                list_iter = node[(-2)]
        assert expr == 'expr'
        assert list_iter == 'list_iter'
        line_number = self.line_number
        last_line = self.f.getvalue().split('\n')[(-1)]
        l = len(last_line)
        indent = ' ' * (l - 1)
        self.preorder(expr)
        line_number = self.indent_if_source_nl(line_number, indent)
        self.preorder(list_iter)
        l2 = self.indent_if_source_nl(line_number, indent)
        if l2 != line_number:
            self.write(' ' * (len(indent) - len(self.indent) - 1) + ']')
        else:
            self.write(' ]')
        self.prec = p
        self.prune()

    def n_list_comp_pypy27(self, node):
        """List comprehensions in PYPY."""
        p = self.prec
        self.prec = 27
        if node[(-1)].kind == 'list_iter':
            n = node[(-1)]
        elif self.is_pypy and node[(-1)] == 'JUMP_BACK':
            n = node[(-2)]
        list_expr = node[1]
        if len(node) >= 3:
            store = node[3]
        elif self.is_pypy and n[0] == 'list_for':
            store = n[0][2]
        assert n == 'list_iter'
        assert store == 'store'
        while n == 'list_iter':
            n = n[0]
            if n == 'list_for':
                n = n[3]
            elif n == 'list_if':
                n = n[2]
            elif n == 'list_if_not':
                n = n[2]

        assert n == 'lc_body'
        self.write('[ ')
        expr = n[0]
        if self.is_pypy and node[(-1)] == 'JUMP_BACK':
            list_iter = node[(-2)]
        else:
            list_iter = node[(-1)]
        assert expr == 'expr'
        assert list_iter == 'list_iter'
        self.preorder(expr)
        self.preorder(list_expr)
        self.write(' ]')
        self.prec = p
        self.prune()

    def comprehension_walk(self, node, iter_index, code_index=-5):
        p = self.prec
        self.prec = 27
        if self.version >= 3.0 and node == 'dict_comp':
            cn = node[1]
        elif self.version <= 2.7 and node == 'generator_exp':
            if node[0] == 'LOAD_GENEXPR':
                cn = node[0]
            elif node[0] == 'load_closure':
                cn = node[1]
        elif self.version >= 3.0 and node in ('generator_exp', 'generator_exp_async'):
            if node[0] == 'load_genexpr':
                load_genexpr = node[0]
            elif node[1] == 'load_genexpr':
                load_genexpr = node[1]
            cn = load_genexpr[0]
        elif hasattr(node[code_index], 'attr'):
            cn = node[code_index]
        elif len(node[1]) > 1 and hasattr(node[1][1], 'attr'):
            cn = node[1][1]
        elif hasattr(node[1][0], 'attr'):
            cn = node[1][0]
        else:
            assert False, "Can't find code for comprehension"
        assert iscode(cn.attr)
        code = Code(cn.attr, self.scanner, self.currentclass)
        ast = self.build_ast(code._tokens, code._customize)
        self.customize(code._customize)
        while len(ast) == 1:
            ast = ast[0]

        n = ast[iter_index]
        assert n == 'comp_iter', n
        while n == 'comp_iter':
            n = n[0]
            if n == 'comp_for':
                if n[0] == 'SETUP_LOOP':
                    n = n[4]
                else:
                    n = n[3]
            elif n == 'comp_if':
                n = n[2]
            elif n == 'comp_if_not':
                n = n[2]

        assert n == 'comp_body', n
        self.preorder(n[0])
        if node == 'generator_exp_async':
            self.write(' async')
            iter_var_index = iter_index - 2
        else:
            iter_var_index = iter_index - 1
        self.write(' for ')
        self.preorder(ast[iter_var_index])
        self.write(' in ')
        if node[2] == 'expr':
            iter_expr = node[2]
        else:
            iter_expr = node[(-3)]
        assert iter_expr == 'expr'
        self.preorder(iter_expr)
        self.preorder(ast[iter_index])
        self.prec = p

    def n_generator_exp(self, node):
        self.write('(')
        iter_index = 3
        if self.version > 3.2:
            code_index = -6
            if self.version > 3.6:
                iter_index = 4
        else:
            code_index = -5
        self.comprehension_walk(node, iter_index=iter_index, code_index=code_index)
        self.write(')')
        self.prune()

    n_generator_exp_async = n_generator_exp

    def n_set_comp(self, node):
        self.write('{')
        if node[0] in ['LOAD_SETCOMP', 'LOAD_DICTCOMP']:
            self.comprehension_walk_newer(node, 1, 0)
        elif node[0].kind == 'load_closure' and self.version >= 3.0:
            self.setcomprehension_walk3(node, collection_index=4)
        else:
            self.comprehension_walk(node, iter_index=4)
        self.write('}')
        self.prune()

    n_dict_comp = n_set_comp

    def comprehension_walk_newer(self, node, iter_index, code_index=-5):
        """Non-closure-based comprehensions the way they are done in Python3
        and some Python 2.7. Note: there are also other set comprehensions.
        """
        p = self.prec
        self.prec = 27
        code = node[code_index].attr
        assert iscode(code), node[code_index]
        code = Code(code, self.scanner, self.currentclass)
        ast = self.build_ast(code._tokens, code._customize)
        self.customize(code._customize)
        while len(ast) == 1 or ast in ('sstmt', 'return') and ast[(-1)] in ('RETURN_LAST',
                                                                            'RETURN_VALUE'):
            self.prec = 100
            ast = ast[0]

        is_30_dict_comp = False
        store = None
        if node == 'list_comp_async':
            n = ast[2][1]
        else:
            n = ast[iter_index]
        if ast in ('set_comp_func', 'dict_comp_func', 'list_comp', 'set_comp_func_header'):
            for k in ast:
                if k == 'comp_iter':
                    n = k
                elif k == 'store':
                    store = k

        else:
            if ast in ('dict_comp', 'set_comp'):
                assert self.version == 3.0
                for k in ast:
                    if k in ('dict_comp_header', 'set_comp_header'):
                        n = k
                    elif k == 'store':
                        store = k
                    elif k == 'dict_comp_iter':
                        is_30_dict_comp = True
                        n = (k[3], k[1])
                    elif k == 'comp_iter':
                        n = k[0]

            elif ast == 'list_comp_async':
                store = ast[2][1]
            else:
                assert n == 'list_iter', n
            if_node = None
            comp_for = None
            comp_store = None
            if n == 'comp_iter':
                comp_for = n
                comp_store = ast[3]
            have_not = False
            while n in ('list_iter', 'comp_iter'):
                if self.version == 3.0 and len(n) == 3:
                    assert n[0] == 'expr' and n[1] == 'expr'
                    n = n[1]
                else:
                    n = n[0]
                if n in ('list_for', 'comp_for'):
                    if n[2] == 'store' and not store:
                        store = n[2]
                    n = n[3]
                elif n in ('list_if', 'list_if_not', 'list_if37', 'list_if37_not',
                           'comp_if', 'comp_if_not'):
                    have_not = n in ('list_if_not', 'comp_if_not', 'list_if37_not')
                    if n in ('list_if37', 'list_if37_not'):
                        n = n[1]
                    else:
                        if_node = n[0]
                        if n[1] == 'store':
                            store = n[1]
                        n = n[2]

        if self.version != 3.0:
            if self.version < 3.7:
                assert n.kind in ('lc_body', 'list_if37', 'comp_body', 'set_comp_func',
                                  'set_comp_body'), ast
            assert store, "Couldn't find store in list/set comprehension"
            if is_30_dict_comp:
                self.preorder(n[0])
                self.write(': ')
                self.preorder(n[1])
            else:
                self.preorder(n[0])
            if node == 'list_comp_async':
                self.write(' async')
                in_node_index = 3
            else:
                in_node_index = -3
            self.write(' for ')
            if comp_store:
                self.preorder(comp_store)
            else:
                self.preorder(store)
            self.write(' in ')
            self.preorder(node[in_node_index])
            if ast == 'list_comp' and self.version != 3.0:
                list_iter = ast[1]
            else:
                raise list_iter == 'list_iter' or AssertionError
            if list_iter[0] == 'list_for':
                self.preorder(list_iter[0][3])
                self.prec = p
                return
        if comp_store:
            self.preorder(comp_for)
        if if_node:
            self.write(' if ')
            if have_not:
                self.write('not ')
            self.prec = 27
            self.preorder(if_node)
        self.prec = p
        return

    def n_listcomp(self, node):
        self.write('[')
        if node[0].kind == 'load_closure':
            assert self.version >= 3.0
            self.listcomp_closure3(node)
        else:
            if node == 'listcomp_async':
                list_iter_index = 5
            else:
                list_iter_index = 1
            self.comprehension_walk_newer(node, list_iter_index, 0)
        self.write(']')
        self.prune()

    def setcomprehension_walk3(self, node, collection_index):
        """Set comprehensions the way they are done in Python3.
        They're more other comprehensions, e.g. set comprehensions
        See if we can combine code.
        """
        p = self.prec
        self.prec = 27
        code = Code(node[1].attr, self.scanner, self.currentclass)
        ast = self.build_ast(code._tokens, code._customize)
        self.customize(code._customize)
        while len(ast) == 1:
            ast = ast[0]

        store = ast[3]
        collection = node[collection_index]
        n = ast[4]
        list_if = None
        assert n == 'comp_iter'
        while n == 'comp_iter':
            n = n[0]
            if n == 'list_for':
                store = n[2]
                n = n[3]
            elif n in ('list_if', 'list_if_not', 'comp_if', 'comp_if_not'):
                if n[0].kind == 'expr':
                    list_if = n
                else:
                    list_if = n[1]
                n = n[(-1)]
            elif n == 'list_if37':
                list_ifs.append(n)
                n = n[(-1)]

        assert n == 'comp_body', ast
        self.preorder(n[0])
        self.write(' for ')
        self.preorder(store)
        self.write(' in ')
        self.preorder(collection)
        if list_if:
            self.preorder(list_if)
        self.prec = p
        return

    def n_classdef(self, node):
        if self.version >= 3.6:
            self.n_classdef36(node)
        elif self.version >= 3.0:
            self.n_classdef3(node)
        cclass = self.currentclass
        if node == 'classdefdeco2':
            build_class = node
        else:
            build_class = node[0]
        build_list = build_class[1][0]
        if hasattr(build_class[(-3)][0], 'attr'):
            subclass_code = build_class[(-3)][0].attr
            class_name = build_class[0].pattr
        elif build_class[(-3)] == 'mkfunc' and node == 'classdefdeco2' and build_class[(-3)][0] == 'load_closure':
            subclass_code = build_class[(-3)][1].attr
            class_name = build_class[(-3)][0][0].pattr
        elif hasattr(node[0][0], 'pattr'):
            subclass_code = build_class[(-3)][1].attr
            class_name = node[0][0].pattr
        else:
            raise 'Internal Error n_classdef: cannot find class name'
        if node == 'classdefdeco2':
            self.write('\n')
        else:
            self.write('\n\n')
        self.currentclass = str(class_name)
        self.write(self.indent, 'class ', self.currentclass)
        self.print_super_classes(build_list)
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

    n_classdefdeco2 = n_classdef

    def print_super_classes(self, node):
        if not node == 'tuple':
            return
        n_subclasses = len(node[:-1])
        if n_subclasses > 0 or self.version > 2.4:
            self.write('(')
        line_separator = ', '
        sep = ''
        for elem in node[:-1]:
            value = self.traverse(elem)
            self.write(sep, value)
            sep = line_separator

        if n_subclasses > 0 or self.version > 2.4:
            self.write(')')

    def print_super_classes3(self, node):
        n = len(node) - 1
        if node.kind != 'expr':
            if node == 'kwarg':
                self.template_engine(('(%[0]{attr}=%c)', 1), node)
                return
            kwargs = None
            assert node[n].kind.startswith('CALL_FUNCTION')
            if node[n].kind.startswith('CALL_FUNCTION_KW'):
                if self.is_pypy:
                    self.template_engine(('(%[0]{attr}=%c)', 1), node[(n - 1)])
                    return
                else:
                    kwargs = node[(n - 1)].attr
                assert isinstance(kwargs, tuple)
                i = n - (len(kwargs) + 1)
                j = 1 + n - node[n].attr
            else:
                i = start = n - 2
                for i in range(start, 0, -1):
                    if node[i].kind not in ['expr', 'call', 'LOAD_CLASSNAME']:
                        break

                if i == start:
                    return
                i += 2
            line_separator = ', '
            sep = ''
            self.write('(')
            if kwargs:
                l = n - 1
            else:
                l = n
            if kwargs:
                while j < i:
                    self.write(sep)
                    value = self.traverse(node[j])
                    self.write('%s' % value)
                    sep = line_separator
                    j += 1

                j = 0
                while i < l:
                    self.write(sep)
                    value = self.traverse(node[i])
                    self.write('%s=%s' % (kwargs[j], value))
                    sep = line_separator
                    j += 1
                    i += 1

            else:
                while i < l:
                    value = self.traverse(node[i])
                    i += 1
                    self.write(sep, value)
                    sep = line_separator

        else:
            if node[0] == 'LOAD_STR':
                return
            value = self.traverse(node[0])
            self.write('(')
            self.write(value)
        self.write(')')
        return

    def kv_map(self, kv_node, sep, line_number, indent):
        first_time = True
        for kv in kv_node:
            assert kv in ('kv', 'kv2', 'kv3')
            if kv == 'kv':
                self.write(sep)
                name = self.traverse(kv[(-2)], indent='')
                if first_time:
                    line_number = self.indent_if_source_nl(line_number, indent)
                    first_time = False
                line_number = self.line_number
                self.write(name, ': ')
                value = self.traverse(kv[1], indent=self.indent + (len(name) + 2) * ' ')
            elif kv == 'kv2':
                self.write(sep)
                name = self.traverse(kv[1], indent='')
                if first_time:
                    line_number = self.indent_if_source_nl(line_number, indent)
                    first_time = False
                line_number = self.line_number
                self.write(name, ': ')
                value = self.traverse(kv[(-3)], indent=self.indent + (len(name) + 2) * ' ')
            elif kv == 'kv3':
                self.write(sep)
                name = self.traverse(kv[(-2)], indent='')
                if first_time:
                    line_number = self.indent_if_source_nl(line_number, indent)
                    first_time = False
                line_number = self.line_number
                self.write(name, ': ')
                line_number = self.line_number
                value = self.traverse(kv[0], indent=self.indent + (len(name) + 2) * ' ')
            self.write(value)
            sep = ', '
            if line_number != self.line_number:
                sep += '\n' + self.indent + '  '
                line_number = self.line_number

    def n_dict(self, node):
        """
        prettyprint a dict
        'dict' is something like k = {'a': 1, 'b': 42}"
        We will source-code use line breaks to guide us when to break.
        """
        p = self.prec
        self.prec = 100
        self.indent_more(INDENT_PER_LEVEL)
        sep = INDENT_PER_LEVEL[:-1]
        if node[0] != 'dict_entry':
            self.write('{')
        line_number = self.line_number
        if self.version >= 3.0 and not self.is_pypy:
            if node[0].kind.startswith('kvlist'):
                kv_node = node[0]
                l = list(kv_node)
                length = len(l)
                if kv_node[(-1)].kind.startswith('BUILD_MAP'):
                    length -= 1
                i = 0
                while i < length:
                    self.write(sep)
                    name = self.traverse(l[i], indent='')
                    if i > 0:
                        line_number = self.indent_if_source_nl(line_number, self.indent + INDENT_PER_LEVEL[:-1])
                    line_number = self.line_number
                    self.write(name, ': ')
                    value = self.traverse(l[(i + 1)], indent=self.indent + (len(name) + 2) * ' ')
                    self.write(value)
                    sep = ', '
                    if line_number != self.line_number:
                        sep += '\n' + self.indent + INDENT_PER_LEVEL[:-1]
                        line_number = self.line_number
                    i += 2

            elif len(node) > 1 and node[1].kind.startswith('kvlist'):
                kv_node = node[1]
                l = list(kv_node)
                if len(l) > 0 and l[0].kind == 'kv3':
                    kv_node = node[1][0]
                    l = list(kv_node)
                i = 0
                while i < len(l):
                    self.write(sep)
                    name = self.traverse(l[(i + 1)], indent='')
                    if i > 0:
                        line_number = self.indent_if_source_nl(line_number, self.indent + INDENT_PER_LEVEL[:-1])
                    line_number = self.line_number
                    self.write(name, ': ')
                    value = self.traverse(l[i], indent=self.indent + (len(name) + 2) * ' ')
                    self.write(value)
                    sep = ', '
                    if line_number != self.line_number:
                        sep += '\n' + self.indent + INDENT_PER_LEVEL[:-1]
                        line_number = self.line_number
                    else:
                        sep += ' '
                    i += 3

            elif node[(-1)].kind.startswith('BUILD_CONST_KEY_MAP'):
                keys = node[(-2)].pattr
                values = node[:-2]
                for (key, value) in zip(keys, values):
                    self.write(sep)
                    self.write(repr(key))
                    line_number = self.line_number
                    self.write(':')
                    self.write(self.traverse(value[0]))
                    sep = ', '
                    if line_number != self.line_number:
                        sep += '\n' + self.indent + INDENT_PER_LEVEL[:-1]
                        line_number = self.line_number
                    else:
                        sep += ' '

                if sep.startswith(',\n'):
                    self.write(sep[1:])
            elif node[0].kind.startswith('dict_entry'):
                assert self.version >= 3.5
                template = ('%C', (0, len(node[0]), ', **'))
                self.template_engine(template, node[0])
                sep = ''
            elif node[(-1)].kind.startswith('BUILD_MAP_UNPACK') or node[(-1)].kind.startswith('dict_entry'):
                assert self.version >= 3.5
                kwargs = node[(-1)].attr
                template = ('**%C', (0, kwargs, ', **'))
                self.template_engine(template, node)
                sep = ''
        else:
            indent = self.indent + '  '
            line_number = self.line_number
            if node[0].kind.startswith('BUILD_MAP'):
                if len(node) > 1 and node[1].kind in ('kvlist', 'kvlist_n'):
                    kv_node = node[1]
                else:
                    kv_node = node[1:]
                self.kv_map(kv_node, sep, line_number, indent)
            else:
                sep = ''
                opname = node[(-1)].kind
                if self.is_pypy and self.version >= 3.5:
                    if opname.startswith('BUILD_CONST_KEY_MAP'):
                        keys = node[(-2)].attr
                        for i in range(len(keys)):
                            key = keys[i]
                            value = self.traverse(node[i], indent='')
                            self.write(sep, key, ': ', value)
                            sep = ', '
                            if line_number != self.line_number:
                                sep += '\n' + self.indent + '  '
                                line_number = self.line_number

                    else:
                        if opname.startswith('kvlist'):
                            list_node = node[0]
                        else:
                            list_node = node
                        assert list_node[(-1)].kind.startswith('BUILD_MAP')
                        for i in range(0, len(list_node) - 1, 2):
                            key = self.traverse(list_node[i], indent='')
                            value = self.traverse(list_node[(i + 1)], indent='')
                            self.write(sep, key, ': ', value)
                            sep = ', '
                            if line_number != self.line_number:
                                sep += '\n' + self.indent + '  '
                                line_number = self.line_number

                elif opname.startswith('kvlist'):
                    kv_node = node[(-1)]
                    self.kv_map(node[(-1)], sep, line_number, indent)
        if sep.startswith(',\n'):
            self.write(sep[1:])
        if node[0] != 'dict_entry':
            self.write('}')
        self.indent_less(INDENT_PER_LEVEL)
        self.prec = p
        self.prune()

    def n_list(self, node):
        """
        prettyprint a list or tuple
        """
        p = self.prec
        self.prec = PRECEDENCE['yield'] - 1
        lastnode = node.pop()
        lastnodetype = lastnode.kind
        last_was_star = self.f.getvalue().endswith('*')
        if lastnodetype.endswith('UNPACK'):
            have_star = True
        else:
            have_star = False
        if lastnodetype.startswith('BUILD_LIST'):
            self.write('[')
            endchar = ']'
        elif lastnodetype.startswith('BUILD_TUPLE'):
            no_parens = False
            for n in node:
                if n == 'expr' and n[0].kind.startswith('build_slice'):
                    no_parens = True
                    break

            if no_parens:
                endchar = ''
            else:
                self.write('(')
                endchar = ')'
        elif lastnodetype.startswith('BUILD_SET'):
            self.write('{')
            endchar = '}'
        elif lastnodetype.startswith('BUILD_MAP_UNPACK'):
            self.write('{*')
            endchar = '}'
        elif lastnodetype.startswith('ROT_TWO'):
            self.write('(')
            endchar = ')'
        else:
            raise TypeError('Internal Error: n_build_list expects list, tuple, set, or unpack')
        flat_elems = flatten_list(node)
        self.indent_more(INDENT_PER_LEVEL)
        sep = ''
        for elem in flat_elems:
            if elem in ('ROT_THREE', 'EXTENDED_ARG'):
                continue
            assert elem == 'expr'
            line_number = self.line_number
            value = self.traverse(elem)
            if line_number != self.line_number:
                sep += '\n' + self.indent + INDENT_PER_LEVEL[:-1]
            elif sep != '':
                sep += ' '
            if not last_was_star:
                if have_star:
                    sep += '*'
            else:
                last_was_star = False
            self.write(sep, value)
            sep = ','

        if lastnode.attr == 1 and lastnodetype.startswith('BUILD_TUPLE'):
            self.write(',')
        self.write(endchar)
        self.indent_less(INDENT_PER_LEVEL)
        self.prec = p
        self.prune()

    n_set = n_tuple = n_build_set = n_list

    def n_store(self, node):
        expr = node[0]
        if expr == 'expr' and expr[0] == 'LOAD_CONST' and node[1] == 'STORE_ATTR':
            node.kind = 'store_w_parens'
        self.default(node)

    def n_unpack(self, node):
        if node[0].kind.startswith('UNPACK_EX'):
            (before_count, after_count) = node[0].attr
            for i in range(before_count + 1):
                self.preorder(node[i])
                if i != 0:
                    self.write(', ')

            self.write('*')
            for i in range(1, after_count + 2):
                self.preorder(node[(before_count + i)])
                if i != after_count + 1:
                    self.write(', ')

            self.prune()
            return
        if node[0] == 'UNPACK_SEQUENCE_0':
            self.write('[]')
            self.prune()
            return
        for n in node[1:]:
            if n[0].kind == 'unpack':
                n[0].kind = 'unpack_w_parens'

        if self.version < 2.7:
            node.kind = 'unpack_w_parens'
        self.default(node)

    n_unpack_w_parens = n_unpack

    def n_attribute(self, node):
        if node[0] == 'LOAD_CONST' or node[0] == 'expr' and node[0][0] == 'LOAD_CONST':
            node.kind = 'attribute_w_parens'
        self.default(node)

    def n_assign(self, node):
        if 3.0 <= self.version <= 3.2 and len(node) == 2:
            if node[0][0] == 'LOAD_FAST' and node[0][0].pattr == '__locals__' and node[1][0].kind == 'STORE_LOCALS':
                self.prune()
        self.default(node)

    def n_assign2(self, node):
        for n in node[-2:]:
            if n[0] == 'unpack':
                n[0].kind = 'unpack_w_parens'

        self.default(node)

    def n_assign3(self, node):
        for n in node[-3:]:
            if n[0] == 'unpack':
                n[0].kind = 'unpack_w_parens'

        self.default(node)

    def n_except_cond2(self, node):
        if node[(-1)] == 'come_from_opt':
            unpack_node = -3
        else:
            unpack_node = -2
        if node[unpack_node][0] == 'unpack':
            node[unpack_node][0].kind = 'unpack_w_parens'
        self.default(node)

    def template_engine(self, entry, startnode):
        """The format template interpetation engine.  See the comment at the
        beginning of this module for the how we interpret format
        specifications such as %c, %C, and so on.
        """
        fmt = entry[0]
        arg = 1
        i = 0
        m = escape.search(fmt)
        while m:
            i = m.end()
            self.write(m.group('prefix'))
            typ = m.group('type') or '{'
            node = startnode
            if m.group('child'):
                node = node[int(m.group('child'))]
            if typ == '%':
                self.write('%')
            elif typ == '+':
                self.line_number += 1
                self.indent_more()
            elif typ == '-':
                self.line_number += 1
                self.indent_less()
            elif typ == '|':
                self.line_number += 1
                self.write(self.indent)
            elif typ == ',':
                if node.kind in ('unpack', 'unpack_w_parens') and node[0].attr == 1:
                    self.write(',')
            elif typ == 'c':
                index = entry[arg]
                if isinstance(index, tuple):
                    assert node[index[0]] == index[1], "at %s[%d], expected '%s' node; got '%s'" % (node.kind, arg, index[1], node[index[0]].kind)
                    index = index[0]
                assert isinstance(index, int), 'at %s[%d], %s should be int or tuple' % (node.kind, arg, type(index))
                self.preorder(node[index])
                arg += 1
            elif typ == 'p':
                p = self.prec
                tup = entry[arg]
                assert isinstance(tup, tuple)
                if len(tup) == 3:
                    (index, nonterm_name, self.prec) = tup
                    assert node[index] == nonterm_name, "at %s[%d], expected '%s' node; got '%s'" % (node.kind, arg, nonterm_name, node[index].kind)
                else:
                    assert len(tup) == 2
                    (index, self.prec) = entry[arg]
                self.preorder(node[index])
                self.prec = p
                arg += 1
            elif typ == 'C':
                (low, high, sep) = entry[arg]
                remaining = len(node[low:high])
                for subnode in node[low:high]:
                    self.preorder(subnode)
                    remaining -= 1
                    if remaining > 0:
                        self.write(sep)

                arg += 1
            elif typ == 'D':
                (low, high, sep) = entry[arg]
                remaining = len(node[low:high])
                for subnode in node[low:high]:
                    remaining -= 1
                    if len(subnode) > 0:
                        self.preorder(subnode)
                        if remaining > 0:
                            self.write(sep)

                arg += 1
            elif typ == 'x':
                assert isinstance(entry[arg], tuple)
                arg += 1
            elif typ == 'P':
                p = self.prec
                (low, high, sep, self.prec) = entry[arg]
                remaining = len(node[low:high])
                for subnode in node[low:high]:
                    self.preorder(subnode)
                    remaining -= 1
                    if remaining > 0:
                        self.write(sep)

                self.prec = p
                arg += 1
            elif typ == '{':
                d = node.__dict__
                expr = m.group('expr')
                if hasattr(node, 'linestart') and node.linestart and hasattr(node, 'current_line_number'):
                    self.source_linemap[self.current_line_number] = node.linestart
                try:
                    self.write(eval(expr, d, d))
                except:
                    raise

            m = escape.search(fmt, i)

        self.write(fmt[i:])

    def default(self, node):
        mapping = self._get_mapping(node)
        table = mapping[0]
        key = node
        for i in mapping[1:]:
            key = key[i]

        if key.kind in table:
            self.template_engine(table[key.kind], node)
            self.prune()

    def customize(self, customize):
        """
        Special handling for opcodes, such as those that take a variable number
        of arguments -- we add a new entry for each in TABLE_R.
        """
        for (k, v) in list(customize.items()):
            if k in TABLE_R:
                continue
            op = k[:k.rfind('_')]
            if k.startswith('CALL_METHOD'):
                TABLE_R[k] = ('%c(%P)', 0, (1, -1, ', ', 100))
            elif self.version >= 3.6 and k.startswith('CALL_FUNCTION_KW'):
                TABLE_R[k] = (
                 '%c(%P)', 0, (1, -1, ', ', 100))
            elif op == 'CALL_FUNCTION':
                TABLE_R[k] = (
                 '%c(%P)', (0, 'expr'), (1, -1, ', ', PRECEDENCE['yield'] - 1))
            elif op in ('CALL_FUNCTION_VAR', 'CALL_FUNCTION_VAR_KW', 'CALL_FUNCTION_KW'):
                if v == 0:
                    str = '%c(%C'
                    p2 = (0, 0, None)
                else:
                    str = '%c(%C, '
                    p2 = (1, -2, ', ')
                if op == 'CALL_FUNCTION_VAR':
                    if self.version == 3.5:
                        if str == '%c(%C, ':
                            entry = (
                             '%c(*%C, %c)', 0, p2, -2)
                        elif str == '%c(%C':
                            entry = (
                             '%c(*%C)', 0, (1, 100, ''))
                    elif self.version == 3.4:
                        if v == 0:
                            str = '%c(*%c)'
                            entry = (str, 0, -2)
                        else:
                            str = '%c(%C, *%c)'
                            entry = (str, 0, p2, -2)
                    else:
                        str += '*%c)'
                        entry = (str, 0, p2, -2)
                elif op == 'CALL_FUNCTION_KW':
                    str += '**%c)'
                    entry = (str, 0, p2, -2)
                elif op == 'CALL_FUNCTION_VAR_KW':
                    str += '*%c, **%c)'
                    na = v & 255
                    if self.version == 3.5 and na == 0:
                        if p2[2]:
                            p2 = (2, -2, ', ')
                        entry = (
                         str, 0, p2, 1, -2)
                    else:
                        if p2[2]:
                            p2 = (1, -3, ', ')
                        entry = (
                         str, 0, p2, -3, -2)
                else:
                    assert False, 'Unhandled CALL_FUNCTION %s' % op
                TABLE_R[k] = entry

        return

    def get_tuple_parameter(self, ast, name):
        """
        If the name of the formal parameter starts with dot,
        it's a tuple parameter, like this:
        #          def MyFunc(xx, (a,b,c), yy):
        #                  print a, b*2, c*42
        In byte-code, the whole tuple is assigned to parameter '.1' and
        then the tuple gets unpacked to 'a', 'b' and 'c'.

        Since identifiers starting with a dot are illegal in Python,
        we can search for the byte-code equivalent to '(a,b,c) = .1'
        """
        assert ast == 'stmts'
        for i in range(len(ast)):
            if ast[i] == 'sstmt':
                node = ast[i][0]
            else:
                node = ast[i]
            if node == 'assign' and node[0] == ASSIGN_TUPLE_PARAM(name):
                del ast[i]
                assert node[1] == 'store'
                result = self.traverse(node[1])
                if not (result.startswith('(') and result.endswith(')')):
                    result = '(%s)' % result
                return result

        raise Exception("Can't find tuple parameter " + name)

    def build_class(self, code):
        """Dump class definition, doc string and class body."""
        assert iscode(code)
        self.classes.append(self.currentclass)
        code = Code(code, self.scanner, self.currentclass)
        indent = self.indent
        ast = self.build_ast(code._tokens, code._customize)
        code._tokens = None
        assert ast == 'stmts'
        if ast[0] == 'sstmt':
            ast[0] = ast[0][0]
        first_stmt = ast[0]
        if ast[0] == 'docstring':
            self.println(self.traverse(ast[0]))
            del ast[0]
        if 3.0 <= self.version <= 3.3:
            try:
                if first_stmt == 'store_locals':
                    if self.hide_internal:
                        del ast[0]
                        if ast[0] == 'sstmt':
                            ast[0] = ast[0][0]
                        first_stmt = ast[0]
            except:
                pass

        try:
            if first_stmt == NAME_MODULE:
                if self.hide_internal:
                    del ast[0]
                    first_stmt = ast[0]
        except:
            pass

        have_qualname = False
        if len(ast):
            if ast[0] == 'sstmt':
                ast[0] = ast[0][0]
            first_stmt = ast[0]
        if self.version < 3.0:
            qualname = ('.').join(self.classes)
            QUAL_NAME = SyntaxTree('assign', [
             SyntaxTree('expr', [Token('LOAD_CONST', pattr=qualname)]), SyntaxTree('store', [Token('STORE_NAME', pattr='__qualname__')])])
            have_qualname = ast[0] == QUAL_NAME
        else:
            try:
                if first_stmt == 'assign' and first_stmt[0][0] == 'LOAD_STR' and first_stmt[1] == 'store' and first_stmt[1][0] == Token('STORE_NAME', pattr='__qualname__'):
                    have_qualname = True
            except:
                pass

        if have_qualname:
            if self.hide_internal:
                del ast[0]
        if code.co_consts and code.co_consts[0] is not None and len(ast) > 0:
            do_doc = False
            if is_docstring(ast[0]):
                i = 0
                do_doc = True
            elif len(ast) > 1 and is_docstring(ast[1]):
                i = 1
                do_doc = True
            if do_doc and self.hide_internal:
                try:
                    docstring = ast[i][0][0][0][0].pattr
                except:
                    docstring = code.co_consts[0]
                else:
                    if print_docstring(self, indent, docstring):
                        self.println()
                        del ast[i]
        if len(ast):
            if ast == 'stmts' and ast[(-1)] == 'sstmt':
                return_locals_parent = ast[(-1)]
                parent_index = 0
            else:
                return_locals_parent = ast
                parent_index = -1
            return_locals = return_locals_parent[parent_index]
            if return_locals == RETURN_LOCALS:
                if self.hide_internal:
                    del return_locals_parent[parent_index]
        (globals, nonlocals) = find_globals_and_nonlocals(ast, set(), set(), code, self.version)
        for g in sorted(globals):
            self.println(indent, 'global ', g)

        for nl in sorted(nonlocals):
            self.println(indent, 'nonlocal ', nl)

        old_name = self.name
        self.gen_source(ast, code.co_name, code._customize)
        self.name = old_name
        code._tokens = None
        code._customize = None
        self.classes.pop(-1)
        return

    def gen_source(self, ast, name, customize, is_lambda=False, returnNone=False):
        """convert SyntaxTree to Python source code"""
        rn = self.return_none
        self.return_none = returnNone
        old_name = self.name
        self.name = name
        if len(ast) == 0:
            self.println(self.indent, 'pass')
        else:
            self.customize(customize)
            if is_lambda:
                self.write(self.traverse(ast, is_lambda=is_lambda))
            else:
                self.text = self.traverse(ast, is_lambda=is_lambda)
                self.println(self.text)
        self.name = old_name
        self.return_none = rn

    def build_ast(self, tokens, customize, is_lambda=False, noneInNames=False, isTopLevel=False):
        if is_lambda:
            for t in tokens:
                if t.kind == 'RETURN_END_IF':
                    t.kind = 'RETURN_END_IF_LAMBDA'
                elif t.kind == 'RETURN_VALUE':
                    t.kind = 'RETURN_VALUE_LAMBDA'

            tokens.append(Token('LAMBDA_MARKER'))
            try:
                p_insts = self.p.insts
                self.p.insts = self.scanner.insts
                self.p.offset2inst_index = self.scanner.offset2inst_index
                ast = python_parser.parse(self.p, tokens, customize)
                self.customize(customize)
                self.p.insts = p_insts
            except python_parser.ParserError, e:
                raise ParserError(e, tokens, self.p.debug['reduce'])
            except AssertionError, e:
                raise ParserError(e, tokens, self.p.debug['reduce'])
            else:
                transform_ast = self.treeTransform.transform(ast)
                self.maybe_show_tree(ast)
                del ast
                return transform_ast
        if self.hide_internal:
            if len(tokens) >= 2:
                if not noneInNames:
                    if tokens[(-1)].kind in ('RETURN_VALUE', 'RETURN_VALUE_LAMBDA'):
                        if tokens[(-2)].kind == 'LOAD_CONST' and (isTopLevel or tokens[(-2)].pattr is None):
                            del tokens[-2:]
                        else:
                            tokens.append(Token('RETURN_LAST'))
                    else:
                        tokens.append(Token('RETURN_LAST'))
            if len(tokens) == 0:
                return PASS
        try:
            p_insts = self.p.insts
            self.p.insts = self.scanner.insts
            self.p.offset2inst_index = self.scanner.offset2inst_index
            self.p.opc = self.scanner.opc
            ast = python_parser.parse(self.p, tokens, customize)
            self.p.insts = p_insts
        except python_parser.ParserError, e:
            raise ParserError(e, tokens, self.p.debug['reduce'])

        checker(ast, False, self.ast_errors)
        self.customize(customize)
        transform_ast = self.treeTransform.transform(ast)
        self.maybe_show_tree(ast)
        del ast
        return transform_ast

    @classmethod
    def _get_mapping(cls, node):
        return MAP.get(node, MAP_DIRECT)


DEFAULT_DEBUG_OPTS = {'asm': False, 'tree': False, 'grammar': False}

def code_deparse(co, out=sys.stdout, version=None, debug_opts=DEFAULT_DEBUG_OPTS, code_objects={}, compile_mode='exec', is_pypy=IS_PYPY, walker=SourceWalker):
    """
    ingests and deparses a given code block 'co'. If version is None,
    we will use the current Python interpreter version.
    """
    assert iscode(co)
    if version is None:
        version = float(sys.version[0:3])
    scanner = get_scanner(version, is_pypy=is_pypy)
    (tokens, customize) = scanner.ingest(co, code_objects=code_objects, show_asm=debug_opts['asm'])
    debug_parser = dict(PARSER_DEFAULT_DEBUG)
    if debug_opts.get('grammar', None):
        debug_parser['reduce'] = debug_opts['grammar']
        debug_parser['errorstack'] = 'full'
    linestarts = dict(scanner.opc.findlinestarts(co))
    deparsed = walker(version, out, scanner, showast=debug_opts.get('ast', None), debug_parser=debug_parser, compile_mode=compile_mode, is_pypy=is_pypy, linestarts=linestarts)
    isTopLevel = co.co_name == '<module>'
    deparsed.ast = deparsed.build_ast(tokens, customize, isTopLevel=isTopLevel)
    if deparsed.ast is None:
        return
    assert deparsed.ast == 'stmts', 'Should have parsed grammar start'
    del tokens
    (deparsed.mod_globs, nonlocals) = find_globals_and_nonlocals(deparsed.ast, set(), set(), co, version)
    assert not nonlocals
    if version >= 3.0:
        load_op = 'LOAD_STR'
    else:
        load_op = 'LOAD_CONST'
    try:
        stmts = deparsed.ast
        first_stmt = stmts[0][0]
        if version >= 3.6:
            if first_stmt[0] == 'SETUP_ANNOTATIONS':
                del stmts[0]
                assert stmts[0] == 'sstmt'
                first_stmt = stmts[0][0]
        if first_stmt == ASSIGN_DOC_STRING(co.co_consts[0], load_op):
            print_docstring(deparsed, '', co.co_consts[0])
            del stmts[0]
        if stmts[(-1)] == RETURN_NONE:
            stmts.pop()
    except:
        pass

    deparsed.FUTURE_UNICODE_LITERALS = COMPILER_FLAG_BIT['FUTURE_UNICODE_LITERALS'] & co.co_flags != 0
    deparsed.gen_source(deparsed.ast, co.co_name, customize)
    for g in sorted(deparsed.mod_globs):
        deparsed.write('# global %s ## Warning: Unused global\n' % g)

    if deparsed.ast_errors:
        deparsed.write('# NOTE: have internal decompilation grammar errors.\n')
        deparsed.write('# Use -t option to show full context.')
        for err in deparsed.ast_errors:
            deparsed.write(err)

        raise SourceWalkerError('Deparsing hit an internal grammar-rule bug')
    if deparsed.ERROR:
        raise SourceWalkerError('Deparsing stopped due to parse error')
    return deparsed


def deparse_code2str(code, out=sys.stdout, version=None, debug_opts=DEFAULT_DEBUG_OPTS, code_objects={}, compile_mode='exec', is_pypy=IS_PYPY, walker=SourceWalker):
    """Return the deparsed text for a Python code object. `out` is where any intermediate
    output for assembly or tree output will be sent.
    """
    return code_deparse(code, out, version, debug_opts, code_objects=code_objects, compile_mode=compile_mode, is_pypy=is_pypy, walker=walker).text


if __name__ == '__main__':

    def deparse_test(co):
        """This is a docstring"""
        s = deparse_code2str(co, debug_opts={'asm': 'after', 'tree': True})
        print s


    deparse_test(deparse_test.func_code)