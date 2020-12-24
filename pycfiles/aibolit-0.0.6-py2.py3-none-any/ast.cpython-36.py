# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/utils/ast.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 665 bytes
from javalang.parse import parse
from javalang.tree import CompilationUnit

class AST:
    __doc__ = '\n    Returns the AST for some java file\n    '

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