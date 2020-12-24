# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dxf2x/dxf.py
# Compiled at: 2019-10-15 11:10:28
# Size of source mod 2**32: 613 bytes
from dxf2x.compiler import syntax, foreach_ast

def lexical(f):
    tokens = []
    for code in f:
        code = code.strip()
        value = f.readline().rstrip('\r\n')
        if code == '0':
            tokens.append({code: value})
        elif tokens:
            tokens[(-1)][code] = value

    return tokens


def read(filename):
    with open(filename, encoding='gbk', errors='ignore') as (f):
        return syntax(lexical(f))


def write(ast, filename):
    with open(filename, 'w', encoding='gbk', errors='ignore') as (f):
        foreach_ast(ast, lambda code, value: f.write(f"{code}\r\n{value}\r\n"))