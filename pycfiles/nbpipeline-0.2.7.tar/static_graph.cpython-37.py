# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/krassowski/nbpipeline/nbpipeline/visualization/static_graph.py
# Compiled at: 2019-06-12 08:27:10
# Size of source mod 2**32: 885 bytes
from os import system
from tempfile import NamedTemporaryFile

def static_graph(rules_dag):
    from networkx.drawing.nx_agraph import to_agraph
    graph = to_agraph(rules_dag)
    graph.node_attr['fontname'] = 'Arial, sans-serf'
    graph.edge_attr['fontname'] = 'Arial, sans-serf'
    with NamedTemporaryFile(suffix='.dot') as (dot_file):
        graph.write(dot_file.name)
    graph.clear()
    with NamedTemporaryFile(mode='r', suffix='.svg') as (temp_file):
        system(f"dot -Tsvg {dot_file.name} -o {temp_file.name}")
        svg = temp_file.read()
        insert_after = 'xmlns:xlink="http://www.w3.org/1999/xlink">'
        processed = svg.replace(insert_after, insert_after + '\n            <style>\n            a:hover polygon {\n                fill: red;\n            }\n            </style>\n        ')
    return processed