# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/instanceof/instance_of.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 930 bytes
import javalang
from aibolit.utils.ast import AST

class InstanceOf:

    def __init__(self):
        pass

    def __traverse_node(self, node):
        """
        Travers over AST tree finds instance_of and .isInstance().
        :param filename:
        :return:
        List of code lines
        """
        lines = []
        for path, node_elem in node.filter(javalang.tree.BinaryOperation):
            if node_elem.operator == 'instanceof':
                code_line = node_elem.operandl.position.line or node_elem.operandr.position.line
                lines.append(code_line)

        for path, node_elem in node.filter(javalang.tree.MethodInvocation):
            if node_elem.member == 'isInstance':
                lines.append(node_elem.position.line)

        return lines

    def value(self, filename: str):
        tree = AST(filename).value()
        return self._InstanceOf__traverse_node(tree)