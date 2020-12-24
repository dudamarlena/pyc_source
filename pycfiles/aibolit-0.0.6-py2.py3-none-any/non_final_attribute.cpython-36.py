# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/patterns/non_final_attribute/non_final_attribute.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 736 bytes
from typing import List
import javalang
from javalang.tree import FieldDeclaration
from aibolit.types_decl import LineNumber

class NonFinalAttribute:

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as (file):
            tree = javalang.parse.parse(file.read())
        return tree

    def value(self, filename: str) -> List[LineNumber]:
        tree = self._NonFinalAttribute__file_to_ast(filename).filter(FieldDeclaration)
        return [node.position.line for path, node in tree if 'final' not in node.modifiers]