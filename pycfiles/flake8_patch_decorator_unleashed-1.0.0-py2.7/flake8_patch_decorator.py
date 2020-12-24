# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flake8_patch_decorator.py
# Compiled at: 2018-11-26 09:07:28
import ast, tokenize
from sys import stdin
__version__ = '1.0.0'
PATCH_DECORATOR_ERROR_CODE = 'T002'
PATCH_DECORATOR_ERROR_MESSAGE = 'use of @patch found (use context manager instead)'

class PatchDecoratorChecker(object):
    name = 'flake8-patch-decorator'
    version = __version__
    ignores = ()

    def __init__(self, tree, filename='(none)', builtins=None):
        self.tree = tree
        self.filename = filename == 'stdin' and stdin or filename

    def run(self):
        if self.filename == stdin:
            noqa = _get_noqa_lines(self.filename)
        else:
            with open(self.filename, 'r') as (file_to_check):
                noqa = _get_noqa_lines(file_to_check.readlines())
        errors = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and hasattr(node, 'decorator_list') and node.decorator_list:
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == 'patch' and decorator.lineno not in noqa:
                        errors.append({'message': ('{0} {1}').format(PATCH_DECORATOR_ERROR_CODE, PATCH_DECORATOR_ERROR_MESSAGE), 
                           'line': decorator.lineno, 
                           'col': decorator.col_offset})

        for error in errors:
            yield (
             error.get('line'), error.get('col'), error.get('message'), type(self))


def _get_noqa_lines(code):
    tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
    return [ token[2][0] for token in tokens if token[0] == tokenize.COMMENT and (token[1].endswith('noqa') or isinstance(token[0], str) and token[0].endswith('noqa'))
           ]