# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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