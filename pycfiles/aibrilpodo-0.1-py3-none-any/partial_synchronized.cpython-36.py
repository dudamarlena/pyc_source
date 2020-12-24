# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/partial_synchronized/partial_synchronized.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 2905 bytes
from collections import defaultdict
import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved

class PartialSync:

    def __init__(self):
        pass

    def value(self, filename):
        total_code_lines = set()
        obj = JavalangImproved(filename)
        empty_lines = obj.get_empty_lines()
        items = obj.tree_to_nodes()
        synch_nodes = defaultdict(list)
        method_nodes = {}
        for x in items:
            if isinstance(x.node, javalang.tree.SynchronizedStatement):
                synch_nodes[x.method_line].append(x)
            else:
                if isinstance(x.node, javalang.tree.MethodDeclaration):
                    method_nodes[x.method_line] = x

        for method_line, sync_nodes in sorted((synch_nodes.items()), key=(lambda x: x[1][0].line)):
            for sync_n in sync_nodes:
                lines = set(range(method_line, sync_n.line))
                empty_lines_before_sync = [x for x in lines if x in empty_lines]
                lines_number_btw_function_and_synch_block = sync_n.line - method_line - len(empty_lines_before_sync)
                if lines_number_btw_function_and_synch_block > 1:
                    total_code_lines.add(sync_n.line)
                    continue
                else:
                    if lines_number_btw_function_and_synch_block == 1:
                        method_item = method_nodes[method_line]
                        if len(method_item.node.body) > 1 and isinstance(method_item.node.body[0], javalang.tree.SynchronizedStatement):
                            total_code_lines.add(sync_n.line)
                            continue

        return sorted(total_code_lines)