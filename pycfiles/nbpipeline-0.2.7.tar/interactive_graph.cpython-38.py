# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/krassowski/nbpipeline/nbpipeline/visualization/interactive_graph.py
# Compiled at: 2019-10-21 14:58:00
# Size of source mod 2**32: 1483 bytes
import json
from collections import defaultdict
from pathlib import Path
from jinja2 import Environment, select_autoescape, FileSystemLoader
from ..graph import Cluster
from ..rules import Group

def render_template(path, **kwargs):
    templates_path = Path(__file__).parent / 'templates'
    env = Environment(loader=(FileSystemLoader(str(templates_path))),
      autoescape=(select_autoescape(['html', 'xml'])))
    template = env.get_template(path)
    return (template.render)(**kwargs)


def assign_to_clusters(rules_dag):
    groups = defaultdict(Cluster)
    for node in rules_dag.nodes:
        if not node.group:
            pass
        else:
            groups[node.group].members.add(node.name)
    else:
        return groups


def generate_graph(rules_dag, **kwargs):
    groups = assign_to_clusters(rules_dag)
    for name, cluster in groups.items():
        if name in Group.groups:
            cluster.group = Group.groups[name]
        else:
            cluster.group = Group(name)
    else:
        json_dag = json.dumps({'nodes':[node.to_json() for node in rules_dag.nodes], 
         'edges':[{'from':edge[0].name, 
          'to':edge[1].name} for edge in rules_dag.edges], 
         'clusters':[cluster.to_json() for cluster in groups.values()]})
        kwargs['json'] = json_dag
        kwargs = {'json': json_dag}
        return render_template(*('graph.html', ), **kwargs)