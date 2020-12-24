# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/patterns/assert_in_code/assert_in_code.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1341 bytes
from typing import List, cast
from javalang.ast import Node
from javalang.tree import CompilationUnit, AssertStatement, ClassDeclaration, BinaryOperation
from aibolit.types_decl import LineNumber
from aibolit.utils.ast import AST
_TEST_CLASS_SUFFIX = 'Test'

class AssertInCode(object):

    def value(self, filename: str) -> List[LineNumber]:
        tree = AST(filename).value()
        return self._AssertInCode__traverse_node(tree)

    def __traverse_node(self, tree: CompilationUnit) -> List[LineNumber]:
        lines = list()
        for path, node in tree.filter(AssertStatement):
            if not _within_test_class(path):
                lines.append(cast(BinaryOperation, node.condition).operandl.position.line)

        return lines


def _within_test_class(path) -> bool:
    class_declaration = next(filter(_is_class_declaration, path[::2]))
    return class_declaration.name.endswith(_TEST_CLASS_SUFFIX)


def _is_class_declaration(node: Node) -> bool:
    return isinstance(node, ClassDeclaration)