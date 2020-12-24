# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/patterns/public_static_method/public_static_method.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 339 bytes
import javalang
from aibolit.utils.ast import AST

class PublicStaticMethod:

    def __init__(self):
        pass

    def value(self, filename: str):
        tree = AST(filename).value().filter(javalang.tree.MethodDeclaration)
        return [node for path, node in tree if all(elem in node.modifiers for elem in ('public',
                                                                                       'static'))]