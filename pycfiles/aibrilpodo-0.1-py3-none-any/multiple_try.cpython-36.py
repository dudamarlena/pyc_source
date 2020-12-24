# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/multiple_try/multiple_try.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 3213 bytes
import javalang
from typing import List
import uuid
from collections import defaultdict
import hashlib, itertools
from aibolit.utils.ast import AST
from javalang.tree import FormalParameter

class MultipleTry:

    def __init__(self):
        pass

    def traverse_node(self, node, dict_with_chains, uuid_method):
        if not node:
            return dict_with_chains
        else:
            for item in node.children:
                if item and (isinstance(item, tuple) or isinstance(item, list)):
                    for j in item:
                        if isinstance(j, javalang.tree.MethodInvocation):
                            if not j.qualifier:
                                if j.qualifier != '':
                                    dict_with_chains[uuid_method].append([j.position.line, j.member])
                                    self.traverse_node(j, dict_with_chains, uuid_method)
                            else:
                                new_uuid = uuid.uuid1()
                                dict_with_chains[new_uuid].append([j.position.line, j.member])
                                self.traverse_node(j, dict_with_chains, new_uuid)
                        else:
                            if isinstance(j, javalang.tree.MethodDeclaration):
                                self.traverse_node(j, dict_with_chains, str(uuid.uuid1()))
                            else:
                                if isinstance(j, javalang.tree.StatementExpression):
                                    self.traverse_node(j, dict_with_chains, uuid_method)
                                else:
                                    if isinstance(j, javalang.tree.This) or isinstance(j, javalang.tree.ClassCreator):
                                        self.traverse_node(j, dict_with_chains, str(uuid.uuid1()))

                else:
                    if isinstance(item, javalang.tree.ClassCreator):
                        self.traverse_node(item, dict_with_chains, uuid_method)

            return dict_with_chains

    def value(self, filename: str):
        """
        Travers over AST tree and fins function with nested/sequential try statement
        :param filename:
        :return:
        List of tuples with LineNumber and List of methods names, e.g.
        [[10, 'func1'], [10, 'fun2']], [[23, 'run'], [23, 'start']]]
        """
        tree = AST(filename).value()
        res = defaultdict(list)
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            for _, try_node in method_node.filter(javalang.tree.TryStatement):
                formal_params = [x.type.name + ' ' + x.name for x in method_node.parameters if isinstance(x, FormalParameter)]
                func_name = '{f}({params})'.format(f=(method_node.name),
                  params=(','.join(formal_params))).encode('utf-8')
                m = hashlib.md5()
                m.update(func_name)
                res[m.hexdigest()].append(method_node.position.line)

        return list(set(itertools.chain.from_iterable([y for x, y in res.items() if len(y) > 1])))