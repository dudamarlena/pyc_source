# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/patterns/supermethod/supermethod.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1827 bytes
import javalang
from aibolit.utils.ast import AST

class SuperMethod:

    def __init__(self):
        pass

    def value(self, filename: str):
        """
        Iterates over functions and finds super.func() calls.
        Javalang doesn't have code line for super.func() call,
        that's why we can only count the first match of a call inside some function.
        It has MULTIPLE MATCHES if we call super.func() inside a ANONYMOUS CLASS.
        :param filename:
        :return: Lines of code
        """
        results = []
        tree = AST(filename).value()
        with open(filename, encoding='utf-8') as (file):
            text_lines = file.readlines()
        for _, method_decl_node in tree.filter(javalang.tree.MethodDeclaration):
            code_line = method_decl_node.position.line
            for _, super_method_inv in method_decl_node.filter(javalang.tree.SuperMethodInvocation):
                str_to_find = 'super.{method_name}('.format(method_name=(super_method_inv.member)).strip()
                for iter, line in enumerate(text_lines[code_line - 1:]):
                    string_strip = line.strip().replace('\n', '').replace('\t', '')
                    if string_strip.find(str_to_find) > -1:
                        results.append(code_line + iter)
                        break

        return results

    def __traverse(self, tree, results):
        descendants = tree.children
        for children in descendants:
            if isinstance(children, tuple) or isinstance(children, list):
                for item in children:
                    if isinstance(item, javalang.tree.SuperMethodInvocation):
                        results.append([item.member])
                    else:
                        self._SuperMethod__traverse(item, results)

        return results