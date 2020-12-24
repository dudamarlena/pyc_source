# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/private_static_method/private_static_method.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 378 bytes
import javalang
from aibolit.utils.ast import AST

class PrivateStaticMethod:

    def __init__(self):
        pass

    def value(self, filename: str):
        return [node.position.line for _, node in AST(filename).value().filter(javalang.tree.MethodDeclaration) if all(elem in node.modifiers for elem in ('private',
                                                                                                                                                           'static'))]