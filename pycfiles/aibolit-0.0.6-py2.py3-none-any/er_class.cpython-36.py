# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/patterns/er_class/er_class.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 761 bytes
import javalang
from aibolit.utils.ast import AST

class ErClass:

    def __init__(self):
        pass

    def value(self, filename: str):
        classes = ('manager', 'controller', 'router', 'dispatcher', 'printer', 'writer',
                   'reader', 'parser', 'generator', 'renderer', 'listener', 'producer',
                   'holder', 'interceptor')
        tree = AST(filename).value().filter(javalang.tree.ClassDeclaration)
        return [node._position.line for _, node in tree if [n for n in classes if n in node.name.lower()] != []]