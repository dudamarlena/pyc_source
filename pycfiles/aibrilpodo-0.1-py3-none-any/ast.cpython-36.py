# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/utils/ast.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 665 bytes
from javalang.parse import parse
from javalang.tree import CompilationUnit

class AST:
    """AST"""

    def __init__(self, filename: str):
        self._filename = filename

    def value(self) -> CompilationUnit:
        """
        @todo #131:30min Introduce tests for AST.value method.
         Currently AST.value method is not being tested. It justs delegates a
         call to javalang library, but we should at least test which kinds of
         file this class should and which it should not support.
        """
        with open((self._filename), encoding='utf-8') as (file):
            return parse(file.read())