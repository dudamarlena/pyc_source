# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/empty_rethrow/empty_rethrow.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 2102 bytes
import javalang
from aibolit.utils.ast import AST

class EmptyRethrow:

    def __init__(self):
        pass

    def value(self, filename):
        tree = AST(filename).value()
        total_code_lines = set()
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            for _, try_node in method_node.filter(javalang.tree.TryStatement):
                for _, throw_node in try_node.filter(javalang.tree.ThrowStatement):
                    if try_node.catches:
                        catch_classes = [x.parameter.name for x in try_node.catches]
                        mem_ref = throw_node.children[1]
                        if isinstance(mem_ref, javalang.tree.ClassCreator):
                            continue
                        elif hasattr(mem_ref, 'member') and mem_ref.member in catch_classes:
                            total_code_lines.add(mem_ref.position.line)

        return sorted(total_code_lines)