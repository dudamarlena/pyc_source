# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/add_non_catalytic_links.py
# Compiled at: 2016-02-16 15:27:04
import sys, os
try:
    from utils import *
except ImportError:
    from sgs_utils.utils import *

import networkx as nx

def usefull_nodes(graph, src, target):
    result = set(nx.predecessor(graph, src).keys())
    graph.reverse(copy=False)
    result = result & set(nx.predecessor(graph, target).keys())
    graph.reverse(copy=False)
    return result


def load_directed_graph(graph_file):
    graph = nx.DiGraph()
    with open(graph_file, 'r') as (in_graph):
        edges = in_graph.read().replace('\r\n', '\n').splitlines()
        for l in edges:
            e = l.split()
            graph.add_edge(e[0], e[1])

    in_graph.close()
    return graph


def main(argv, prog=os.path.basename(sys.argv[0])):
    import argparse, textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('\t\tGenerate the reaction graph of a metabolic network from a list of reactions in .tsv file format.\n\n\t\texemple:\n\t\t%(prog)s reaction_graph catalyze\n\t\t'), prog=prog)
    parser.add_argument('reaction_graph_file', help='Reaction graph file')
    parser.add_argument('catalyze_file', help='Reaction/Gene catalytic association file (.tsv)')
    parser.add_argument('output_reaction_graph_file', help='The output reaction graph')
    parser.add_argument('uncatalyzed_edge_file', help="The list of uncatalyzed 'shortcut' edges")
    parser.add_argument('-k', '--keep_non_catalytic_reactions', action='store_true', default=False, help='Keep the vertices (and related edges) corresponding to non catalytic reactions')
    args = parser.parse_args(argv)
    reaction_graph = load_directed_graph(args.reaction_graph_file)
    map_reaction_to_gene = load_map_id_to_set(args.catalyze_file, silent_warning=True)
    uncatalyzed_reaction_set = set(reaction_graph.nodes()) - set(map_reaction_to_gene.keys())
    uncatalyzed_subgraph = reaction_graph.subgraph(uncatalyzed_reaction_set)
    map_annotation_non_catalytic_edge = {}
    for cc in nx.connected_components(nx.Graph(uncatalyzed_subgraph)):
        for s in cc:
            catalytic_predecessor = []
            for v in reaction_graph.predecessors(s):
                if v not in uncatalyzed_reaction_set:
                    catalytic_predecessor.append(v)

            for t in cc:
                catalytic_successor = []
                for v in reaction_graph.successors(t):
                    if v not in uncatalyzed_reaction_set:
                        catalytic_successor.append(v)

                temp = usefull_nodes(uncatalyzed_subgraph, s, t)
                if temp:
                    for rs in catalytic_predecessor:
                        for rt in catalytic_successor:
                            if rs != rt and not reaction_graph.has_edge(rs, rt):
                                if (
                                 rs, rt) not in map_annotation_non_catalytic_edge:
                                    map_annotation_non_catalytic_edge[(rs, rt)] = set()
                                map_annotation_non_catalytic_edge[(rs, rt)].update(temp)

    for s, t in map_annotation_non_catalytic_edge.keys():
        reaction_graph.add_edge(s, t)

    if not args.keep_non_catalytic_reactions:
        reaction_graph.remove_nodes_from(uncatalyzed_reaction_set)
    output = open(args.output_reaction_graph_file, 'w')
    for s, t in reaction_graph.edges():
        output.write('%s\t%s\n' % (s, t))

    output.close()
    output = open(args.uncatalyzed_edge_file, 'w')
    for s, t in map_annotation_non_catalytic_edge.keys():
        output.write('%s\t%s\t%s\n' % (s, t, (' ').join(sorted(map_annotation_non_catalytic_edge[(s, t)]))))

    output.close()
    sys.stderr.write('Info: %d vertices and %d arcs; %d non-catalytic arcs\n' % (reaction_graph.number_of_nodes(), reaction_graph.number_of_edges(), len(map_annotation_non_catalytic_edge)))


if __name__ == '__main__':
    main(sys.argv[1:])