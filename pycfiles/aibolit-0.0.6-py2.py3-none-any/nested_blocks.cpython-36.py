# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/patterns/nested_blocks/nested_blocks.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 4023 bytes
import javalang
from javalang.tree import Node
from typing import List, Callable, Optional, Any
from aibolit.utils.ast import AST

class BlockType:
    FOR = javalang.tree.ForStatement
    IF = javalang.tree.IfStatement
    WHILE = javalang.tree.WhileStatement
    DO = javalang.tree.DoStatement


class NestedBlocks:
    __doc__ = '\n    Returns lines in the file where\n    nested blocks statements are located\n    '

    def __init__(self, max_depth: int, block_type=BlockType.FOR):
        self.max_depth = max_depth
        self.block_type = block_type if isinstance(block_type, list) else [block_type]

    def __for_node_depth(self, tree: javalang.ast.Node, max_depth: int, for_links: List=[], for_before: int=0) -> None:
        """
        Takes AST tree and returns list of "FOR" AST nodes of depth greater
        or equal than max_depth
        """
        if type(tree) in self.block_type:
            for_before += 1
            if for_before >= max_depth:
                for_links += [tree]
        for child in tree.children:
            nodes_arr = child if isinstance(child, list) else [child]
            for node in nodes_arr:
                if not hasattr(node, 'children'):
                    pass
                else:
                    self._NestedBlocks__for_node_depth(node, max_depth, for_links, for_before)

    def __fold_traverse_tree(self, root: javalang.ast.Node, f: Callable[([javalang.ast.Node], Optional[Any])]) -> List[Any]:
        """
        Traverse AST tree and apply function to each node
        Accumulate results in the list and return
        """
        res = []
        v = f(root)
        if v is not None:
            res.append(v)
        for child in root.children:
            nodes_arr = child if isinstance(child, list) else [child]
            for node in nodes_arr:
                if not hasattr(node, 'children'):
                    pass
                else:
                    res += self._NestedBlocks__fold_traverse_tree(node, f)

        return res

    def value(self, filename: str) -> List[int]:
        """Return line numbers in the file where patterns are found"""
        tree = AST(filename).value()
        for_links = []
        self._NestedBlocks__for_node_depth(tree,
          max_depth=(self.max_depth),
          for_links=for_links)

        def find_line_position(node: Node) -> Optional[int]:
            if hasattr(node, '_position'):
                return node._position.line
            else:
                return

        n_lines = [self._NestedBlocks__fold_traverse_tree(for_node, find_line_position) for for_node in for_links]
        n_lines = [v for v in n_lines if len(v) > 0]
        return list(map(min, n_lines))