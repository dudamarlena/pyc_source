# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/reporters/nodegraph/text.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 937 bytes
from dexy.reporter import Reporter

class PlainTextGraph(Reporter):
    __doc__ = '\n    Emits a plain text graph of the network structure.\n    '
    aliases = ['graph']
    _settings = {'in-cache-dir':True, 
     'filename':'graph.txt', 
     'run-for-wrapper-states':[
      'ran', 'checked']}

    def run(self, wrapper):
        self.wrapper = wrapper

        def print_inputs(node, indent=0):
            content = []
            s = ' ' * indent * 4
            content.append('%s%s (%s)' % (s, node, node.state))
            for child in list(node.inputs) + node.children:
                content.extend(print_inputs(child, indent + 1))

            return content

        graph = []
        for node in wrapper.roots:
            graph.extend(print_inputs(node))

        self.create_cache_reports_dir()
        with open(self.report_file(), 'w') as (f):
            f.write('\n'.join(graph) + '\n')