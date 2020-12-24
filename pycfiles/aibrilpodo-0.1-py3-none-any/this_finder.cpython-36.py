# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/this_finder/this_finder.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 5140 bytes
import javalang
from aibolit.utils.ast import AST

class ThisFinder:

    def __expr_stat(self, expr, flag_this, flag_else):
        """function to work with StatementExpression block"""
        if isinstance(expr.expression, javalang.tree.ExplicitConstructorInvocation):
            if flag_this + flag_else > 0:
                return (1, flag_this, flag_else)
            flag_this = 1
        elif flag_this > 0:
            return (1, flag_this, flag_else)
        flag_else = 1
        return (
         0, flag_this, flag_else)

    def __try_stat(self, expr, flag_this, flag_else):
        """function to work with TryStatement block"""
        if expr.resources is not None or expr.catches[0].block != [] or expr.finally_block is not None:
            flag_else = 1
        try_exprs = expr.block
        for expr1 in try_exprs:
            if isinstance(expr1, javalang.tree.StatementExpression):
                res, flag_this, flag_else = self._ThisFinder__expr_stat(expr1, flag_this, flag_else)
                if res > 0:
                    return (1, flag_this, flag_else)
            else:
                if flag_this > 0:
                    return (1, flag_this, flag_else)
                flag_else = 1

        flag_else = 1
        return (
         0, flag_this, flag_else)

    def __if_stat(self, expr, flag_this, flag_else):
        """function to work with IfStatement block"""
        if expr.then_statement is not None:
            res, flag_this, flag_else = self._ThisFinder__work_with_stats(expr.then_statement.statements, flag_this, flag_else)
            if res > 0:
                return (1, flag_this, flag_else)
        if expr.else_statement is not None:
            if isinstance(expr.else_statement, javalang.tree.IfStatement):
                res, flag_this, flag_else = self._ThisFinder__if_stat(expr.else_statement, flag_this, flag_else)
                if res > 0:
                    return (1, flag_this, flag_else)
                else:
                    return (
                     0, flag_this, flag_else)
            block = expr.else_statement
            res, flag_this, flag_else = self._ThisFinder__work_with_stats(block, flag_this, flag_else)
            if res > 0:
                return (1, flag_this, flag_else)
        return (
         0, flag_this, flag_else)

    def __work_with_stats(self, stats, flag_this, flag_else):
        """function to work with objects in constructor"""
        for expr in stats:
            res = 0
            old_else = flag_else
            flag_else = 1
            if isinstance(expr, javalang.tree.TryStatement):
                res, flag_this, flag_else = self._ThisFinder__try_stat(expr, flag_this, old_else)
            else:
                if isinstance(expr, javalang.tree.StatementExpression):
                    res, flag_this, flag_else = self._ThisFinder__expr_stat(expr, flag_this, old_else)
                else:
                    if isinstance(expr, javalang.tree.IfStatement):
                        res, flag_this, flag_else = self._ThisFinder__if_stat(expr, flag_this, flag_else)
                    else:
                        if isinstance(expr, javalang.tree.ForStatement):
                            res, flag_this, flag_else = self._ThisFinder__work_with_stats(expr.body.statements, flag_this, flag_else)
                        else:
                            if isinstance(expr, javalang.tree.WhileStatement):
                                res, flag_this, flag_else = self._ThisFinder__work_with_stats(expr.body.statements, flag_this, flag_else)
                            else:
                                if isinstance(expr, javalang.tree.DoStatement):
                                    res, flag_this, flag_else = self._ThisFinder__work_with_stats(expr.body.statements, flag_this, flag_else)
                                else:
                                    res = flag_this
            if res > 0:
                return (1, flag_this, flag_else)

        return (
         0, flag_this, flag_else)

    def value(self, filename: str):
        """main function"""
        tree = AST(filename).value()
        num_str = []
        for path, node in tree.filter(javalang.tree.ConstructorDeclaration):
            number = node.position.line
            stats = node.children[(-1)]
            result, _, _ = self._ThisFinder__work_with_stats(stats, 0, 0)
            if result == 1:
                num_str.append(number)

        return sorted(list(set(num_str)))