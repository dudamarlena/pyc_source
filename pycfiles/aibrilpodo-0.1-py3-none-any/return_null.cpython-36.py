# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/return_null/return_null.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 2166 bytes
from collections import defaultdict
from aibolit.utils.ast import AST
import javalang

class ReturnNull:

    def __init__(self):
        pass

    def value(self, filename: str):
        """
        Travers over AST tree and finds pattern
        :param filename:
        """
        tree = AST(filename).value()
        chain_lst = defaultdict(int)
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            for _, return_node in method_node.filter(javalang.tree.ReturnStatement):
                return_literal = return_node.children[1]
                if isinstance(return_literal, javalang.tree.Literal) and return_literal.value == 'null':
                    chain_lst[method_node.name] = return_literal.position.line or return_node.position.line
                else:
                    if isinstance(return_literal, javalang.tree.TernaryExpression):
                        chain_lst[method_node.name] = return_node.position.line

        filtered_dict = list(filter(lambda elem: elem > 0, chain_lst.values()))
        return filtered_dict