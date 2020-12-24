# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/helper.py
# Compiled at: 2020-04-27 23:06:35
import sys
from xdis import iscode
from uncompyle6.parsers.treenode import SyntaxTree
from uncompyle6 import PYTHON3
if PYTHON3:
    from itertools import zip_longest
    minint = -sys.maxsize - 1
    maxint = sys.maxsize
else:
    minint = -sys.maxint - 1
    maxint = sys.maxint
    try:
        from itertools import izip_longest as zip_longest
    except:
        from itertools import chain, izip, repeat

        def zip_longest(*args, **kwds):
            fillvalue = kwds.get('fillvalue')

            def sentinel(counter=([fillvalue] * (len(args) - 1)).pop):
                yield counter()

            fillers = repeat(fillvalue)
            iters = [ chain(it, sentinel(), fillers) for it in args ]
            try:
                for tup in izip(*iters):
                    yield tup

            except IndexError:
                pass


read_write_global_ops = frozenset(('STORE_GLOBAL', 'DELETE_GLOBAL', 'LOAD_GLOBAL'))
read_global_ops = frozenset(('STORE_GLOBAL', 'DELETE_GLOBAL'))
nonglobal_ops = frozenset(('STORE_DEREF', 'DELETE_DEREF'))

def escape_string(s, quotes=('"', "'", '"""', "'''")):
    quote = None
    for q in quotes:
        if s.find(q) == -1:
            quote = q
            break

    if quote is None:
        quote = '"""'
        s = s.replace('"""', '\\"""')
    for (orig, replace) in (('\t', '\\t'), ('\n', '\\n'), ('\r', '\\r')):
        s = s.replace(orig, replace)

    return '%s%s%s' % (quote, s, quote)


def find_all_globals(node, globs):
    """Search Syntax Tree node to find variable names that are global."""
    for n in node:
        if isinstance(n, SyntaxTree):
            globs = find_all_globals(n, globs)
        elif n.kind in read_write_global_ops:
            globs.add(n.pattr)

    return globs


def find_code_node(node, start):
    for i in range(-start, len(node) + 1):
        if node[(-i)].kind == 'LOAD_CODE':
            code_node = node[(-i)]
            assert iscode(code_node.attr)
            return code_node

    assert False, 'did not find code node starting at %d in %s' % (start, node)


def find_globals_and_nonlocals(node, globs, nonlocals, code, version):
    """search a node of parse tree to find variable names that need a
    either 'global' or 'nonlocal' statements added."""
    for n in node:
        if isinstance(n, SyntaxTree):
            (globs, nonlocals) = find_globals_and_nonlocals(n, globs, nonlocals, code, version)
        elif n.kind in read_global_ops:
            globs.add(n.pattr)
        elif version >= 3.0 and n.kind in nonglobal_ops and n.pattr in code.co_freevars and n.pattr != code.co_name and code.co_name != '<lambda>':
            nonlocals.add(n.pattr)

    return (
     globs, nonlocals)


def find_none(node):
    for n in node:
        if isinstance(n, SyntaxTree):
            if n not in ('return_stmt', 'return_if_stmt'):
                if find_none(n):
                    return True
        elif n.kind == 'LOAD_CONST' and n.pattr is None:
            return True

    return False


def flatten_list(node):
    """
    List of expressions may be nested in groups of 32 and 1024
    items. flatten that out and return the list
    """
    flat_elems = []
    for elem in node:
        if elem == 'expr1024':
            for subelem in elem:
                assert subelem == 'expr32'
                for subsubelem in subelem:
                    flat_elems.append(subsubelem)

        elif elem == 'expr32':
            for subelem in elem:
                assert subelem == 'expr'
                flat_elems.append(subelem)

        else:
            flat_elems.append(elem)

    return flat_elems


def gen_function_parens_adjust(mapping_key, node):
    """If we can avoid the outer parenthesis
    of a generator function, set the node key to
    'call_generator' and the caller will do the default
    action on that. Otherwise we do nothing.
    """
    if mapping_key.kind != 'CALL_FUNCTION_1':
        return
    args_node = node[(-2)]
    if args_node == 'pos_arg':
        assert args_node[0] == 'expr'
        n = args_node[0][0]
        if n == 'generator_exp':
            node.kind = 'call_generator'


def print_docstring(self, indent, docstring):
    quote = '"""'
    if docstring.find(quote) >= 0:
        if docstring.find("'''") == -1:
            quote = "'''"
    self.write(indent)
    if not PYTHON3 and not isinstance(docstring, str):
        self.write('u')
        docstring = repr(docstring.expandtabs())[2:-1]
    elif PYTHON3 and 2.4 <= self.version <= 2.7:
        try:
            repr(docstring.expandtabs())[1:-1].encode('ascii')
        except UnicodeEncodeError:
            self.write('u')
        else:
            docstring = repr(docstring.expandtabs())[1:-1]
    else:
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
    return True


def strip_quotes(s):
    if s.startswith("'''") and s.endswith("'''"):
        s = s[3:-3]
    elif s.startswith('"""') and s.endswith('"""'):
        s = s[3:-3]
    elif s.startswith("'") and s.endswith("'"):
        s = s[1:-1]
    elif s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    return s