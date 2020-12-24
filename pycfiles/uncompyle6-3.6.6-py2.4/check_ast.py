# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/check_ast.py
# Compiled at: 2019-04-13 23:34:13
"""
Python parse tree checker.

Our rules sometimes give erroneous results. Until we have perfect rules,
This checker will catch mistakes in decompilation we've made.

FIXME idea: extend parsing system to do same kinds of checks or nonterminal
before reduction and don't reduce when there is a problem.
"""

def checker(ast, in_loop, errors):
    if ast is None:
        return
    in_loop = in_loop or ast.kind in ('while1stmt', 'whileTruestmt', 'whilestmt', 'whileelsestmt',
                                      'while1elsestmt', 'for_block') or ast.kind.startswith('async_for')
    if ast.kind in ('aug_assign1', 'aug_assign2') and ast[0][0] == 'and':
        text = str(ast)
        error_text = '\n# improper augmented assigment (e.g. +=, *=, ...):\n#\t' + ('\n# ').join(text.split('\n')) + '\n'
        errors.append(error_text)
    for node in ast:
        if not in_loop and node.kind in ('continue', 'break'):
            text = str(node)
            error_text = '\n# not in loop:\n#\t' + ('\n# ').join(text.split('\n'))
            errors.append(error_text)
        if hasattr(node, '__repr1__'):
            checker(node, in_loop, errors)

    return