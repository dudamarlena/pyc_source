# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fstringify/transform.py
# Compiled at: 2019-10-18 01:02:30
# Size of source mod 2**32: 7422 bytes
import ast, re, astor
from fstringify.utils import MOD_KEY_PATTERN, MOD_KEY_NAME_PATTERN, VAR_KEY_PATTERN

def handle_from_mod_dict_name(node):
    """Convert a `BinOp` `%` formatted str with a name representing a Dict on the right to an f-string.

    Takes an ast.BinOp representing `"1. %(key1)s 2. %(key2)s" % mydict`
    and converted it to a ast.JoinedStr representing `f"1. {mydict['key1']} 2. {mydict['key2']}"`

    Args:
       node (ast.BinOp): The node to convert to a f-string

    Returns ast.JoinedStr (f-string)
    """
    format_str = node.left.s
    matches = MOD_KEY_PATTERN.findall(format_str)
    var_keys = []
    for idx, m in enumerate(matches):
        var_key = MOD_KEY_NAME_PATTERN.match(m)
        if not var_key:
            raise ValueError('could not find dict key')
        var_keys.append(var_key[1])

    result_node = ast.JoinedStr()
    result_node.values = []
    var_keys.reverse()
    blocks = MOD_KEY_PATTERN.split(format_str)
    for block in blocks:
        if MOD_KEY_PATTERN.match(block):
            fv = ast.FormattedValue(value=ast.Subscript(value=(node.right),
              slice=ast.Index(value=ast.Str(s=(var_keys.pop())))),
              conversion=(-1),
              format_spec=None)
            result_node.values.append(fv)
        else:
            result_node.values.append(ast.Str(s=block))

    return result_node


def handle_from_mod_tuple(node):
    """Convert a `BinOp` `%` formatted str with a tuple on the right to an f-string.

    Takes an ast.BinOp representing `"1. %s 2. %s" % (a, b)`
    and converted it to a ast.JoinedStr representing `f"1. {a} 2. {b}"`

    Args:
       node (ast.BinOp): The node to convert to a f-string

    Returns ast.JoinedStr (f-string)
    """
    format_str = node.left.s
    matches = VAR_KEY_PATTERN.findall(format_str)
    if len(node.right.elts) != len(matches):
        raise ValueError('string formatting length mismatch')
    str_vars = list(map(lambda x: x, node.right.elts))
    result_node = ast.JoinedStr()
    result_node.values = []
    str_vars.reverse()
    blocks = VAR_KEY_PATTERN.split(format_str)
    for block in blocks:
        if VAR_KEY_PATTERN.match(block):
            fv = ast.FormattedValue(value=(str_vars.pop()),
              conversion=(-1),
              format_spec=None)
            result_node.values.append(fv)
        else:
            result_node.values.append(ast.Str(s=block))

    return result_node


def handle_from_mod_generic_name(node):
    """Convert a `BinOp` `%` formatted str with a unknown name on the `node.right` to an f-string.

    When `node.right` is a Name since we don't know if it's a single var or a dict so we sniff the string.

    `"val: %(key_name1)s val2: %(key_name2)s" % some_dict`
    Sniffs the left string for Dict style usage and calls: `handle_from_mod_dict_name`

    `"val: %s" % some_var`
    Borrow the core logic by injecting the name into a ast.Tuple

    Args:
       node (ast.BinOp): The node to convert to a f-string

    Returns ast.JoinedStr (f-string)
    """
    has_dict_str_format = MOD_KEY_PATTERN.findall(node.left.s)
    if has_dict_str_format:
        return handle_from_mod_dict_name(node)
    else:
        node.right = ast.Tuple(elts=[node.right])
        return handle_from_mod_tuple(node)


def handle_from_mod(node):
    if isinstance(node.right, (ast.Name, ast.Attribute, ast.Str, ast.Call)):
        return handle_from_mod_generic_name(node)
    else:
        if isinstance(node.right, ast.Tuple):
            return handle_from_mod_tuple(node)
        if isinstance(node.right, ast.Dict):
            return node
    raise RuntimeError('unexpected `node.right` class')


class FstringifyTransformer(ast.NodeTransformer):

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.lineno = -1
        self.col_offset = -1

    def visit_BinOp(self, node):
        """Convert `ast.BinOp` to `ast.JoinedStr` f-string

        Currently only if a string literal `ast.Str` is on the left side of the `%`
        and one of `ast.Tuple`, `ast.Name`, `ast.Dict` is on the right

        Args:
            node (ast.BinOp): The node to convert to a f-string

        Returns ast.JoinedStr (f-string)
        """
        do_change = isinstance(node.left, ast.Str) and isinstance(node.op, ast.Mod) and isinstance(node.right, (ast.Tuple, ast.Name, ast.Attribute, ast.Str, ast.Call))
        if do_change:
            no_good = [
             '}', '{', '\n']
            for ng in no_good:
                if ng in node.left.s:
                    return node

            for ch in ast.walk(node.right):
                if isinstance(ch, ast.BinOp):
                    return node
                if isinstance(ch, ast.Str):
                    if any(map(lambda x: x in ch.s, ('\n', '\t', '\r', "'", '"', '%s',
                                                     '%%'))) or '\\' in ch.s:
                        return node

        if do_change:
            self.counter += 1
            self.lineno = node.lineno
            self.col_offset = node.col_offset
            result_node = handle_from_mod(node)
            return result_node
        else:
            return node


def fstringify_node(node, debug=False):
    ft = FstringifyTransformer()
    result = ft.visit(node)
    return (
     result,
     dict(changed=(ft.counter > 0),
       lineno=(ft.lineno),
       col_offset=(ft.col_offset),
       skip=True))


def fstringify_code(code, include_meta=False, debug=False):
    """Convert a block of with a %-formatted string to an f-string

    Args:
        code (str): The code to convert.

    Returns:
       The code formatted with f-strings if possible if it's left unchanged.
    """
    converted = None
    meta = dict(changed=False, lineno=1, col_offset=(-22), skip=True)
    code_strip = code.strip()
    if code_strip == '' or code_strip.startswith('#'):
        meta['skip'] = True
        return (code, meta if include_meta else code)
    try:
        tree = ast.parse(code)
        converted, meta = fstringify_node(tree, debug=debug)
    except SyntaxError as e:
        meta['skip'] = code.rstrip().endswith(':') or 'cannot include a blackslash' in str(e)
    except Exception as e2:
        meta['skip'] = False

    if meta['changed'] and converted:
        new_code = astor.to_source(converted)
        if include_meta:
            return (
             new_code, meta)
        return new_code
    else:
        if include_meta:
            return (
             code, meta)
        return code