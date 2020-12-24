# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dbryan/.virtualenvs/ssg/lib/python3.4/site-packages/salt_state_graph/__init__.py
# Compiled at: 2015-08-03 01:29:57
# Size of source mod 2**32: 3673 bytes
import json, pydot, sys

def find(obj, find_key):
    """
    Takes a list and a set.  Returns a list of all matching objects.

    Uses find_inner to recursively traverse the data structure, finding objects
    with keyed by find_key.
    """
    all_matches = [find_inner(item, find_key) for item in obj]
    final = [item for sublist in all_matches for item in sublist]
    return final


def find_inner(obj, find_key):
    """
    Recursively search through the data structure to find objects
    keyed by find_key.
    """
    results = []
    if not hasattr(obj, '__iter__'):
        return results
    if isinstance(obj, dict):
        for key, prop in obj.items():
            if key == find_key:
                results.extend(prop)
            elif isinstance(prop, dict):
                results.extend(find_inner(prop, find_key))
                continue

    elif isinstance(obj, list):
        for i in obj:
            results.extend(find_inner(i, find_key))

    return results


def make_node_name(state_type, state_label):
    return '{0} - {1}'.format(state_type.upper(), state_label)


def find_edges(states, relname):
    """
    Use find() to recursively find objects at keys matching
    relname, yielding a node name for every result.
    """
    try:
        deps = find(states, relname)
        for dep in deps:
            for dep_type, dep_name in dep.items():
                yield make_node_name(dep_type, dep_name)

    except AttributeError as e:
        sys.stderr.write('Bad state: {0}\n'.format(str(states)))
        raise e


class Graph(object):

    def __init__(self, input):
        state_obj = json.load(input)
        self.graph = pydot.Dot('states', graph_type='digraph')
        rules = {'require': {'color': 'blue'},  'require_in': {'color': 'blue',  'reverse': True},  'watch': {'color': 'red'},  'watch_in': {'color': 'red',  'reverse': True}}
        if len(state_obj.keys()) > 1:
            raise Exception('Unsupported: graph for multiple minions: {}'.format(','.join(state_obj)))
        minion_obj = list(state_obj.values())[0]
        for top_key, props in minion_obj.items():
            if top_key == '__extend__':
                sys.stderr.write('Removing __extend__ states:\n{0}\n'.format(str(props)))
                continue
            for top_key_type, states in list(props.items()):
                if top_key_type[:2] == '__':
                    continue
                node_name = make_node_name(top_key_type, top_key)
                self.graph.add_node(pydot.Node(node_name))
                for edge_type, ruleset in list(rules.items()):
                    for relname in find_edges(states, edge_type):
                        if 'reverse' in ruleset and ruleset['reverse']:
                            self.graph.add_edge(pydot.Edge(node_name, relname, color=ruleset['color']))
                        else:
                            self.graph.add_edge(pydot.Edge(relname, node_name, color=ruleset['color']))

    def render(self, fmt):
        if fmt == 'dot':
            return self.graph.to_string()