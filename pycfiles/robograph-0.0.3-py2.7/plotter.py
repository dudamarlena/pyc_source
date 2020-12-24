# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/nodes/plotter.py
# Compiled at: 2016-07-13 17:51:17
import networkx as nx, matplotlib.pyplot as plt

def prepare_plot(graph):
    """
    Prepares a Matplotlib plot for further handling
    :param graph: datamodel.base.Graph instance
    :return: None
    """
    G = graph.nxgraph
    depth_levels_from_root = nx.shortest_path_length(G, graph.root_node)
    vmax = 1.0
    colormap = plt.get_cmap('BuGn')
    step = 1.0 / len(graph)
    node_colors = [ vmax - step * depth_levels_from_root[n] for n in G.nodes() ]
    pos = nx.spectral_layout(G)
    nx.draw_networkx_labels(G, pos, labels=dict([ (n, n.name) for n in G.nodes() ]), font_weight='bold', font_color='orangered')
    nx.draw_networkx_nodes(G, pos, node_size=2000, cmap=colormap, vmin=0.0, vmax=vmax, node_color=node_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=dict([ ((u, v), d['name']) for u, v, d in G.edges(data=True) ]))
    nx.draw_networkx_edges(G, pos, edgelist=[ edge for edge in G.edges() ], arrows=True)


def show_plot(graph):
    """
    Shows a plot of the graph
    :param graph: datamodel.base.Graph instance
    :return: None
    """
    prepare_plot(graph)
    try:
        plt.show()
    except KeyboardInterrupt:
        plt.close()


def save_plot(graph, outputfile):
    """
    Saves the plot of the graph to an image file (eg: PNG)
    :param graph: datamodel.base.Graph instance
    :param outputfile: path of output file
    :return: None
    """
    prepare_plot(graph)
    plt.savefig(outputfile)
    plt.close()