# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/reporters/nodegraph/graphviz.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1227 bytes
from dexy.reporter import Reporter

class Graphviz(Reporter):
    __doc__ = '\n    Emits a graphviz graph of the network structure.\n    '
    aliases = ['graphviz', 'nodegraph']
    _settings = {'in-cache-dir':True, 
     'filename':'graph.dot', 
     'run-for-wrapper-states':[
      'ran', 'checked', 'error']}

    def run(self, wrapper):
        self.wrapper = wrapper

        def print_children(node, indent=0):
            content = []
            content.append(node.key)
            for child in node.children:
                for line in print_children(child, indent + 1):
                    content.append(line)

            return content

        def print_inputs(node):
            content = []
            for child in node.inputs:
                content.extend(print_inputs(child))
                content.append('"%s" -> "%s";' % (node, child))

            return content

        graph = []
        graph.append('digraph G {')
        for node in list(wrapper.nodes.values()):
            graph.extend(print_inputs(node))

        graph.append('}')
        self.create_cache_reports_dir()
        with open(self.report_file(), 'w') as (f):
            f.write('\n'.join(graph))