# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/redundant_catch/redundant_catch.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 4400 bytes
import itertools
from collections import defaultdict
from collections import namedtuple
import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved
ExceptionInfo = namedtuple('ExceptionInfo', 'func_name, catch_list, throws_list, line_number')

class RedundantCatch:
    """RedundantCatch"""

    def __init__(self):
        pass

    def value(self, filename):
        """
        Find the mentioned-above pattern
        :param filename: filename of Java file
        :return: code lines of try statement where it was found
        """
        total_code_lines = set()
        obj = JavalangImproved(filename)
        items = obj.tree_to_nodes()
        try_nodes = defaultdict(list)
        method_nodes = {}
        for x in items:
            is_instance_meth_decl = isinstance(x.node, javalang.tree.MethodDeclaration)
            is_instance_try_stat = isinstance(x.node, javalang.tree.TryStatement)
            is_instance_ctor_decl = isinstance(x.node, javalang.tree.ConstructorDeclaration)
            is_instance_lambda = isinstance(x.node, javalang.tree.LambdaExpression)
            if is_instance_try_stat and x.method_line and not is_instance_lambda:
                try_nodes[x.method_line].append(x)
            else:
                if (is_instance_meth_decl or is_instance_ctor_decl) and x.method_line and not is_instance_lambda:
                    method_nodes[x.method_line] = x

        for method_line, iter_nodes in sorted((try_nodes.items()), key=(lambda x: x[1][0].line)):
            for try_node in iter_nodes:
                method_node = method_nodes.get(method_line)
                if not not method_node:
                    if not method_node.node.throws:
                        pass
                    else:
                        catch_list = []
                        ei = ExceptionInfo(func_name=(method_node.node.name),
                          catch_list=catch_list,
                          throws_list=(method_node.node.throws),
                          line_number=(method_node.node.position.line))
                        if try_node.node.catches:
                            catch_classes = [x.parameter.types for x in try_node.node.catches]
                            classes_exception_list = list((itertools.chain)(*catch_classes))
                            ei.catch_list.extend(classes_exception_list)
                            lines_number = set([try_node.line for c in ei.catch_list if c in ei.throws_list])
                            total_code_lines.update(lines_number)

        return sorted(total_code_lines)