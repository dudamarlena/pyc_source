# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/force_type_casting_finder/force_type_casting_finder.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 2528 bytes
import javalang
from aibolit.utils.ast import AST

class ForceTypeCastingFinder:

    def __process_node(self, node):
        line = node.position.line if (hasattr(node, 'position') and node.position is not None) else None
        qualifier = node.qualifier if hasattr(node, 'qualifier') else None
        member = node.member if hasattr(node, 'member') else None
        name = node.name if hasattr(node, 'name') else None
        return {'line':line, 
         'name':qualifier or member or name, 
         'ntype':type(node)}

    def __tree_to_list(self, tree: javalang.tree.CompilationUnit):
        """Convert AST tree to list of object"""
        items = [self._ForceTypeCastingFinder__process_node(node) for path, node in tree if node is not None]
        last_line_number = None
        for item in items:
            if item['line'] is not None:
                last_line_number = item['line']
            else:
                item['line'] = last_line_number

        return items

    def value(self, filename: str):
        """"""
        tree = AST(filename).value()
        list_tree = self._ForceTypeCastingFinder__tree_to_list(tree)
        num_str = []
        for node in list_tree:
            if node['ntype'] == javalang.tree.Cast:
                k = int(node['line'])
                if k not in num_str:
                    num_str.append(k)

        return num_str