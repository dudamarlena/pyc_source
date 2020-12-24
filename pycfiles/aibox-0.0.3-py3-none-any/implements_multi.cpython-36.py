# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/implements_multi/implements_multi.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 339 bytes
import javalang
from aibolit.utils.ast import AST

class ImplementsMultiFinder:

    def __init__(self):
        pass

    def value(self, filename: str):
        tree = AST(filename).value().filter(javalang.tree.ClassDeclaration)
        return [node._position.line for _, node in tree if node.implements if len(node.implements) > 1]