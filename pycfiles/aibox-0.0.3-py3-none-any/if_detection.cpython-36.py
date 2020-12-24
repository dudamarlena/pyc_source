# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/if_return_if_detection/if_detection.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1020 bytes
import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved

class newJavalangImproved(JavalangImproved):

    def filter(self, ntypes):
        nodes = self.tree_to_nodes()
        array = []
        for index, i in enumerate(nodes):
            if type(i.node) in ntypes and type(i.node.then_statement) in [javalang.tree.BlockStatement] and i.node.else_statement is not None:
                for check_return in i.node.then_statement.statements:
                    if type(check_return) in [javalang.tree.ReturnStatement]:
                        array.append(nodes[index].line + 1)

        return array


class CountIfReturn:
    """CountIfReturn"""

    def __init__(self):
        pass

    def value(self, filename: str):
        """"""
        tree = newJavalangImproved(filename)
        if_decls = tree.filter([javalang.tree.IfStatement])
        return if_decls