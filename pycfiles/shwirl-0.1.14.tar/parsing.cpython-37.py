# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/shaders/parsing.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 4531 bytes
from __future__ import division
import re
re_type = '(?:void|int|float|vec2|vec3|vec4|mat2|mat3|mat4|\\\n            sampler1D|sampler2D|sampler3D)'
re_identifier = '(?:[a-zA-Z_][\\w_]*)'
re_qualifier = '(const|uniform|attribute|varying)'
re_template_var = '(?:(?:\\$' + re_identifier + ')|(?:\\$\\{' + re_identifier + '\\}))'
re_func_name = '(' + re_identifier + '|' + re_template_var + ')'
re_declaration = '(?:(' + re_type + ')\\s+(' + re_identifier + '))'
re_prog_var_declaration = '(?:' + re_qualifier + '?\\s*(' + re_type + ')\\s+(' + re_identifier + '(\\s*,\\s*(' + re_identifier + '))*))'
re_arg_list = '(' + re_declaration + '(?:,\\s*' + re_declaration + ')*)?'
re_func_decl = '(' + re_type + ')\\s+' + re_func_name + '\\s*\\((void|' + re_arg_list + ')\\)'
re_anon_decl = '(?:(' + re_type + ')(?:\\s+' + re_identifier + ')?)'
re_anon_arg_list = '(' + re_anon_decl + '(?:,\\s*' + re_anon_decl + ')*)?'
re_func_prot = '(' + re_type + ')\\s+' + re_func_name + '\\((void|' + re_anon_arg_list + ')\\)\\s*;'

def parse_function_signature(code):
    """
    Return the name, arguments, and return type of the first function
    definition found in *code*. Arguments are returned as [(type, name), ...].
    """
    m = re.search('^\\s*' + re_func_decl + '\\s*{', code, re.M)
    if m is None:
        print(code)
        raise Exception('Failed to parse function signature. Full code is printed above.')
    else:
        rtype, name, args = m.groups()[:3]
        if args == 'void' or args.strip() == '':
            args = []
        else:
            args = [tuple(arg.strip().split(' ')) for arg in args.split(',')]
    return (
     name, args, rtype)


def find_functions(code):
    """
    Return a list of (name, arguments, return type) for all function 
    definition2 found in *code*. Arguments are returned as [(type, name), ...].
    """
    regex = '^\\s*' + re_func_decl + '\\s*{'
    funcs = []
    while True:
        m = re.search(regex, code, re.M)
        if m is None:
            return funcs
        else:
            rtype, name, args = m.groups()[:3]
            if args == 'void' or args.strip() == '':
                args = []
            else:
                args = [tuple(arg.strip().split(' ')) for arg in args.split(',')]
        funcs.append((name, args, rtype))
        code = code[m.end():]


def find_prototypes(code):
    """
    Return a list of signatures for each function prototype declared in *code*.
    Format is [(name, [args], rtype), ...].
    """
    prots = []
    lines = code.split('\n')
    for line in lines:
        m = re.match('\\s*' + re_func_prot, line)
        if m is not None:
            rtype, name, args = m.groups()[:3]
            if args == 'void' or args.strip() == '':
                args = []
            else:
                args = [tuple(arg.strip().split(' ')) for arg in args.split(',')]
            prots.append((name, args, rtype))

    return prots


def find_program_variables(code):
    """
    Return a dict describing program variables::

        {'var_name': ('uniform|attribute|varying', type), ...}

    """
    vars = {}
    lines = code.split('\n')
    for line in lines:
        m = re.match('\\s*' + re_prog_var_declaration + '\\s*(=|;)', line)
        if m is not None:
            vtype, dtype, names = m.groups()[:3]
            for name in names.split(','):
                vars[name.strip()] = (
                 vtype, dtype)

    return vars


def find_template_variables(code):
    """
    Return a list of template variables found in *code*.

    """
    return re.findall(re_template_var, code)