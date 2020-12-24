# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/patterns/null_check/null_check.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 2339 bytes
from typing import List, Tuple, Type
from javalang.ast import Node
from javalang.tree import CompilationUnit, BinaryOperation, Expression, Literal, ConstructorDeclaration
from aibolit.types_decl import LineNumber
from aibolit.utils.ast import AST
Path = Tuple
_OP_EQUAL = '=='
_OP_NOT_EQUAL = '!='
_LT_NULL = 'null'

class NullCheck(object):

    def value(self, filename: str) -> List[LineNumber]:
        tree = AST(filename).value()
        return self._traverse_node(tree)

    def _traverse_node(self, tree: CompilationUnit) -> List[LineNumber]:
        lines = list()
        for path, node in tree.filter(BinaryOperation):
            if _is_null_check(node) and not _within_constructor(path):
                lines.append(node.operandr.position.line)

        return lines


def _is_null_check(node: BinaryOperation) -> bool:
    return node.operator in (_OP_EQUAL, _OP_NOT_EQUAL) and _is_null(node.operandr)


def _is_null(node: Expression) -> bool:
    return isinstance(node, Literal) and node.value == _LT_NULL


def _within_constructor(path: Path) -> bool:
    node_types = [type(p) for p in path[::2]]
    return ConstructorDeclaration in node_types