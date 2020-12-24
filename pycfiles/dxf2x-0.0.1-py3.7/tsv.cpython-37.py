# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dxf2x/tsv.py
# Compiled at: 2019-10-15 11:10:34
# Size of source mod 2**32: 805 bytes
from dxf2x.compiler import syntax, foreach_ast

def lexical(f):
    return [{code:value for code, value in [word.split(':', 1) for word in line.rstrip('\n').split('\t')]} for line in f if line.startswith('0:')]


def read(filename):
    with open(filename, errors='ignore') as (f):
        return syntax(lexical(f))


def write(ast, filename):
    with open(filename, 'w', errors='ignore') as (fout):
        is_empty = True

        def word_consumer(code, value):
            nonlocal is_empty
            if is_empty:
                is_empty = False
            else:
                fout.write('\n' if code == '0' else '\t')
            fout.write(f"{code}:{value}")

        foreach_ast(ast, word_consumer)
        fout.write('\n')