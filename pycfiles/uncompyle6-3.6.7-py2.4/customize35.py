# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/customize35.py
# Compiled at: 2020-04-18 17:55:36
"""Isolate Python 3.5 version-specific semantic actions here.
"""
from xdis import iscode
from xdis.util import co_flags_is_async
from uncompyle6.semantics.consts import INDENT_PER_LEVEL, PRECEDENCE, TABLE_DIRECT
from uncompyle6.semantics.helper import flatten_list, gen_function_parens_adjust

def customize_for_version35(self, version):
    TABLE_DIRECT.update({'await_expr': ('await %p', (0, PRECEDENCE['await_expr'] - 1)), 'await_stmt': ('%|%c\n', 0), 'async_for_stmt': ('%|async for %c in %c:\n%+%|%c%-\n\n', 9, 1, 25), 'async_forelse_stmt': ('%|async for %c in %c:\n%+%c%-%|else:\n%+%c%-\n\n', 9, 1, 25, (27, 'else_suite')), 'async_with_stmt': ('%|async with %c:\n%+%c%-', (0, 'expr'), 3), 'async_with_as_stmt': ('%|async with %c as %c:\n%+%c%-', (0, 'expr'), (2, 'store'), 3), 'unmap_dict': ('{**%C}', (0, -1, ', **'))})

    def async_call(node):
        self.f.write('async ')
        node.kind == 'call'
        p = self.prec
        self.prec = 80
        self.template_engine(('%c(%P)', 0, (1, -4, ', ', 100)), node)
        self.prec = p
        node.kind == 'async_call'
        self.prune()

    self.n_async_call = async_call

    def n_build_list_unpack(node):
        """
        prettyprint a list or tuple
        """
        p = self.prec
        self.prec = 100
        lastnode = node.pop()
        lastnodetype = lastnode.kind
        last_was_star = self.f.getvalue().endswith('*')
        if lastnodetype.startswith('BUILD_LIST'):
            self.write('[')
            endchar = ']'
        flat_elems = flatten_list(node)
        self.indent_more(INDENT_PER_LEVEL)
        sep = ''
        for elem in flat_elems:
            if elem in ('ROT_THREE', 'EXTENDED_ARG'):
                continue
            assert elem == 'expr'
            line_number = self.line_number
            use_star = True
            value = self.traverse(elem)
            if value.startswith('('):
                assert value.endswith(')')
                use_star = False
                value = value[1:-1].rstrip(' ')
                if value == '':
                    pass
                elif value.endswith(','):
                    value = value[:-1]
            if line_number != self.line_number:
                sep += '\n' + self.indent + INDENT_PER_LEVEL[:-1]
            elif sep != '':
                sep += ' '
            if not last_was_star and use_star:
                sep += '*'
            else:
                last_was_star = False
            self.write(sep, value)
            sep = ','

        self.write(endchar)
        self.indent_less(INDENT_PER_LEVEL)
        self.prec = p
        self.prune()

    self.n_build_list_unpack = n_build_list_unpack

    def n_call(node):
        p = self.prec
        self.prec = 100
        mapping = self._get_mapping(node)
        table = mapping[0]
        key = node
        for i in mapping[1:]:
            key = key[i]

        if key.kind.startswith('CALL_FUNCTION_VAR_KW'):
            entry = table[key.kind]
            kwarg_pos = entry[2][1]
            args_pos = kwarg_pos - 1
            while node[kwarg_pos] == 'kwarg' and kwarg_pos < len(node):
                node[kwarg_pos], node[args_pos] = node[args_pos], node[kwarg_pos]
                args_pos = kwarg_pos
                kwarg_pos += 1

        elif key.kind.startswith('CALL_FUNCTION_VAR'):
            argc = node[(-1)].attr
            nargs = argc & 255
            kwargs = argc >> 8 & 255
            if nargs > 0:
                template = (
                 '%c(%P, ', 0, (1, nargs + 1, ', ', 100))
            else:
                template = ('%c(', 0)
            self.template_engine(template, node)
            args_node = node[(-2)]
            if args_node in ('pos_arg', 'expr'):
                args_node = args_node[0]
            if args_node == 'build_list_unpack':
                template = (
                 '*%P)', (0, len(args_node) - 1, ', *', 100))
                self.template_engine(template, args_node)
            else:
                if len(node) - nargs > 3:
                    template = (
                     '*%c, %P)', nargs + 1, (nargs + kwargs + 1, -1, ', ', 100))
                else:
                    template = (
                     '*%c)', nargs + 1)
                self.template_engine(template, node)
            self.prec = p
            self.prune()
        else:
            gen_function_parens_adjust(key, node)
        self.prec = 100
        self.default(node)

    self.n_call = n_call

    def is_async_fn(node):
        code_node = node[0][0]
        for n in node[0]:
            if hasattr(n, 'attr') and iscode(n.attr):
                code_node = n
                break

        is_code = hasattr(code_node, 'attr') and iscode(code_node.attr)
        return is_code and co_flags_is_async(code_node.attr.co_flags)

    def n_function_def(node):
        if is_async_fn(node):
            self.template_engine(('\n\n%|async def %c\n', -2), node)
        else:
            self.default(node)
        self.prune()

    self.n_function_def = n_function_def

    def n_mkfuncdeco0(node):
        if is_async_fn(node):
            self.template_engine(('%|async def %c\n', 0), node)
        else:
            self.default(node)
        self.prune()

    self.n_mkfuncdeco0 = n_mkfuncdeco0

    def unmapexpr(node):
        last_n = node[0][(-1)]
        for n in node[0]:
            self.preorder(n)
            if n != last_n:
                self.f.write(', **')

        self.prune()

    self.n_unmapexpr = unmapexpr

    def n_list_unpack(node):
        """
        prettyprint an unpacked list or tuple
        """
        p = self.prec
        self.prec = 100
        lastnode = node.pop()
        lastnodetype = lastnode.kind
        last_was_star = self.f.getvalue().endswith('*')
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
            if elem[0] == 'tuple':
                assert value[0] == '('
                assert value[(-1)] == ')'
                value = value[1:-1]
                if value[(-1)] == ',':
                    value = value[:-1]
            else:
                value = '*' + value
            if line_number != self.line_number:
                sep += '\n' + self.indent + INDENT_PER_LEVEL[:-1]
            elif sep != '':
                sep += ' '
            if not last_was_star:
                pass
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

    self.n_tuple_unpack = n_list_unpack