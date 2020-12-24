# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo93/mogo/mptt_graph/templatetags/mptt_graph_tags.py
# Compiled at: 2018-02-15 04:13:01
# Size of source mod 2**32: 1266 bytes
import importlib
from django import template
register = template.Library()

def recurse_nodes(node, previous_node=None, previous_nodename=''):
    output = []
    if previous_node is None:
        node_name = 'node_' + str(node.level)
    else:
        node_name = 'node_' + str(previous_node.level)
    if node.level == 0:
        output.append('var ' + node_name + ' = new Object();')
        output.append(node_name + '.Content = "' + node.name + '";')
        output.append(node_name + '.Nodes = new Array();')
    content = ''
    for descendant in node.get_children():
        content = content + 'Content: "' + descendant.name + '",'
        output.append(recurse_nodes(descendant, previous_node=node, previous_nodename=node_name))

    output.append(node_name + '.Nodes[' + previous_nodename + '] = { ' + content + ' };')
    return '\n'.join(output)


@register.inclusion_tag('mptt_graph/tree.html')
def get_tree(modelpath, node=1):
    t = modelpath.split('.')
    modelname = t[(-1)]
    t.pop()
    path = '.'.join(t)
    module = importlib.import_module(path)
    model = getattr(module, modelname)
    root_node = model.objects.get(pk=21)
    output = recurse_nodes(root_node)
    return {'output': output}