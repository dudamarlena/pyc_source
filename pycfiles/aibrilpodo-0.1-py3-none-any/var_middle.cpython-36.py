# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/var_middle/var_middle.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 9609 bytes
from typing import List, Tuple
from enum import Enum
from functools import reduce
import javalang
from aibolit.types_decl import LineNumber
NODE_KEYWORD_MAP = {'SuperMethodInvocation':'super', 
 'WhileStatement':'while', 
 'ForStatement':'for', 
 'TryStatement':'try', 
 'CatchClause':'catch', 
 'SynchronizedStatement':'synchronized'}
NEW_SCOPE_NODES = [
 javalang.tree.MethodDeclaration,
 javalang.tree.IfStatement,
 javalang.tree.ForStatement,
 javalang.tree.SwitchStatement,
 javalang.tree.TryStatement,
 javalang.tree.DoStatement,
 javalang.tree.WhileStatement,
 javalang.tree.BlockStatement,
 javalang.tree.CatchClause,
 javalang.tree.SynchronizedStatement]

class ASTNode:

    def __init__(self, line, method_line, node, scope):
        self.line = line
        self.method_line = method_line
        self.node = node
        self.scope = scope


class JavalangImproved:

    def __init__(self, filename: str):
        tree, lines = self._JavalangImproved__file_to_ast(filename)
        self.tree = tree
        self.lines = lines

    def __file_to_ast(self, filename: str) -> Tuple[(javalang.ast.Node, List[str])]:
        """Takes path to java class file and returns AST Tree"""
        with open(filename, encoding='utf-8') as (file):
            tree = javalang.parse.parse(file.read())
        with open(filename, encoding='utf-8') as (file):
            lines = file.readlines()
        return (
         tree, lines)

    def __find_keyword(self, lines, keyword, start):
        """
        Args:
            lines (List[str]): List of lines from parsed source code file
            keyword (str): keyword to find
            start (int): Line number to start search
        """
        for i in range(start - 1, len(lines)):
            if keyword in lines[i]:
                return i + 1

        return -1

    def __fix_line_number_if_possible(self, node: javalang.ast.Node, line_n):
        """
        Try to figure out the "true" line number of AST node in the source file
        """
        node_class_name = node.__class__.__name__
        if node_class_name not in NODE_KEYWORD_MAP:
            return line_n
        else:
            line = self._JavalangImproved__find_keyword(self.lines, NODE_KEYWORD_MAP[node_class_name], line_n)
            if line == -1:
                return line_n
            return line

    def __tree_to_nodes(self, tree: javalang.ast.Node, line=1, parent_method_line=None, scope=0) -> List[ASTNode]:
        """
        Return AST nodes with line numbers sorted by line number

        Args:
            tree (javalang.ast.Node): AST node
            line (int): Supposed line number of processed AST node in the file
            parent_method_line (int): Nearest line number of the method this node located
            scope (int): ID of scope processed AST node located
        """
        if hasattr(tree, 'position'):
            if tree.position:
                line = tree.position.line
        else:
            line = self._JavalangImproved__fix_line_number_if_possible(tree, line)
            if type(tree) in NEW_SCOPE_NODES:
                scope += 1
            if type(tree) in [javalang.tree.MethodDeclaration,
             javalang.tree.ConstructorDeclaration,
             javalang.tree.LambdaExpression]:
                parent_method_line = line
        res = []
        for child in tree.children:
            nodes_arr = child if isinstance(child, list) else [child]
            for node in nodes_arr:
                if not hasattr(node, 'children'):
                    pass
                else:
                    left_siblings_line = res[(-1)].line if len(res) > 0 else line
                    res += self._JavalangImproved__tree_to_nodes(node, left_siblings_line, parent_method_line, scope)

        return [ASTNode(line, parent_method_line, tree, scope)] + res

    def tree_to_nodes(self) -> List[ASTNode]:
        """Return AST nodes as list with line numbers sorted by line number"""
        nodes = self._JavalangImproved__tree_to_nodes(self.tree)
        return sorted(nodes, key=(lambda v: v.line))

    def filter(self, ntypes: List[javalang.tree.Node]) -> List[ASTNode]:
        nodes = self.tree_to_nodes()
        return list(filter(lambda v: type(v.node) in ntypes, nodes))

    def get_empty_lines(self) -> List[int]:
        """Figure out lines that are either empty or multiline statements"""
        lines_with_nodes = self.get_non_empty_lines()
        max_line = max(lines_with_nodes)
        return list(set(range(1, max_line + 1)).difference(lines_with_nodes))

    def get_non_empty_lines(self) -> List[int]:
        """Figure out file lines that contains statements"""
        return list(map(lambda v: v.line, self.tree_to_nodes()))


class NodeType(Enum):
    OTHER = 1
    VAR = 2
    SCOPE = 3


class VarMiddle:
    """VarMiddle"""

    def __init__(self):
        pass

    def __check_var_declaration(self, var_idx: int, nodes_list) -> bool:
        """
        Check that VAR declaration line is near the beginning of its scope
        Args:
            pos (int): Line number we are going to check.
            nodes_list (List): List of nodes

        Returns:
            bool: True if VAR declaration is near the begining of the scope
        """
        line, ntype, scope = nodes_list[var_idx]
        if ntype != NodeType.VAR:
            raise ValueError('Variable declaration line is expected!')
        i = var_idx - 1
        while i >= 0:
            _line, _ntype, _scope = nodes_list[i]
            if scope != _scope:
                return False
            if _ntype == NodeType.SCOPE:
                return True
            if _ntype == NodeType.OTHER:
                return False
            i -= 1

        raise ValueError('Method declaration is not found')

    def _prepare_nodes(self, tree: JavalangImproved) -> List[Tuple[(int, NodeType, int)]]:
        to_ignore = [
         javalang.tree.FormalParameter,
         javalang.tree.ReferenceType,
         javalang.tree.BasicType]
        var_node_type = [
         javalang.tree.LocalVariableDeclaration,
         javalang.tree.TryResource]
        scope_node_type = NEW_SCOPE_NODES
        nodes = tree.tree_to_nodes()
        nodes = list(filter(lambda n: type(n.node) not in to_ignore, nodes))

        def node_to_type(node):
            if type(node.node) in var_node_type:
                return NodeType.VAR
            else:
                if type(node.node) in scope_node_type:
                    return NodeType.SCOPE
                return NodeType.OTHER

        def cmp_node(ntype1: NodeType, ntype2: NodeType):
            if ntype1.value > ntype2.value:
                return True
            else:
                return False

        def reduce_f(accum, val):
            if len(accum) == 0:
                accum.append(val)
            else:
                if accum[(-1)].line != val.line or accum[(-1)].scope != val.scope:
                    accum.append(val)
                accum[-1] = cmp_node(node_to_type(accum[(-1)]), node_to_type(val)) or val
            return accum

        nodes = reduce(reduce_f, nodes, [])
        return [(e.line, node_to_type(e), e.scope) for e in nodes]

    def value(self, filename: str) -> List[LineNumber]:
        tree = JavalangImproved(filename)
        nodes = self._prepare_nodes(tree)
        line_matches = []
        for i, (line, node, _) in enumerate(nodes):
            if node != NodeType.VAR:
                pass
            else:
                if not self._VarMiddle__check_var_declaration(i, nodes):
                    line_matches.append(line)

        return line_matches