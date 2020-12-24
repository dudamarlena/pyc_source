# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/infomap/examples/python/example-networkx.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 2124 bytes
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from infomap import infomap

def findCommunities(G):
    """
        Partition network with the Infomap algorithm.
        Annotates nodes with 'community' id and return number of communities found.
        """
    infomapWrapper = infomap.Infomap('--two-level')
    print('Building Infomap network from a NetworkX graph...')
    for e in G.edges():
        (infomapWrapper.addLink)(*e)

    print('Find communities with Infomap...')
    infomapWrapper.run()
    tree = infomapWrapper.tree
    print('Found %d top modules with codelength: %f' % (tree.numTopModules(), tree.codelength()))
    communities = {}
    for node in tree.leafIter():
        communities[node.originalLeafIndex] = node.moduleIndex()

    nx.set_node_attributes(G, name='community', values=communities)
    return tree.numTopModules()


def drawNetwork(G):
    pos = nx.spring_layout(G)
    communities = [v for k, v in nx.get_node_attributes(G, 'community').items()]
    numCommunities = max(communities) + 1
    cmapLight = colors.ListedColormap(['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#cab2d6'], 'indexed', numCommunities)
    cmapDark = colors.ListedColormap(['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a'], 'indexed', numCommunities)
    nx.draw_networkx_edges(G, pos)
    nodeCollection = nx.draw_networkx_nodes(G, pos=pos,
      node_color=communities,
      cmap=cmapLight)
    darkColors = [cmapDark(v) for v in communities]
    nodeCollection.set_edgecolor(darkColors)
    for n in G.nodes():
        plt.annotate(n, xy=(pos[n]),
          textcoords='offset points',
          horizontalalignment='center',
          verticalalignment='center',
          xytext=[
         0, 2],
          color=(cmapDark(communities[n])))

    plt.axis('off')
    plt.show()


G = nx.karate_club_graph()
findCommunities(G)
drawNetwork(G)