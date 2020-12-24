# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/multiple_while/multiple_while.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 638 bytes
import javalang
from aibolit.utils.ast import AST

class MultipleWhile:

    def __init__(self):
        pass

    def value(self, filename: str):
        """
        Travers over AST tree and finds function with sequential while statement
        :param filename:
        :return:
        List of LineNumber of methods which have sequential while statements
        """
        res = []
        for _, method_node in AST(filename).value().filter(javalang.tree.MethodDeclaration):
            if len(list(method_node.filter(javalang.tree.WhileStatement))) > 1:
                res.append(method_node.position.line)

        return res