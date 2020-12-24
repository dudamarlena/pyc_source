# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/many_primary_ctors/many_primary_ctors.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 2252 bytes
from typing import List
import javalang.ast, javalang.parse, javalang.tree
from aibolit.types_decl import LineNumber
from aibolit.utils.ast import AST

class ManyPrimaryCtors(object):

    def value(self, filename: str):
        tree = AST(filename).value()
        return self._ManyPrimaryCtors__traverse_node(tree)

    def __traverse_node(self, tree: javalang.ast.Node) -> List[LineNumber]:
        lines = list()
        for _, class_declaration in tree.filter(javalang.tree.ClassDeclaration):
            primary_ctors = list(filter(_is_primary, class_declaration.constructors))
            if len(primary_ctors) > 1:
                lines.extend(ctor.position.line for ctor in primary_ctors)

        return lines


def _is_primary(constructor: javalang.tree.ConstructorDeclaration) -> bool:
    for _, assignment in constructor.filter(javalang.tree.Assignment):
        if _is_instance_variable_assignment(assignment):
            return True

    return False


def _is_instance_variable_assignment(assignment: javalang.tree.Assignment) -> bool:
    return isinstance(assignment.expressionl, javalang.tree.This)