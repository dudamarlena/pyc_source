# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/patterns/non_final_class/non_final_class.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 510 bytes
from typing import List
from javalang.tree import ClassDeclaration
from aibolit.types_decl import LineNumber
from aibolit.utils.ast import AST

class NonFinalClass:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        tree = AST(filename).value()
        classes = tree.filter(ClassDeclaration)
        return [node.position.line for _, node in classes if len([v for v in ('final',
                                                                              'abstract') if v in node.modifiers]) == 0]