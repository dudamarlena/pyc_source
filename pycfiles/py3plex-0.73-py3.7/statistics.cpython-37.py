# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/statistics/statistics.py
# Compiled at: 2019-09-30 13:55:18
# Size of source mod 2**32: 1615 bytes
import networkx as nx, pandas as pd

def core_network_statistics(G, labels=None, name='example'):
    rframe = pd.DataFrame(columns=['Name',
     'classes',
     'nodes',
     'edges',
     'degree',
     'diameter',
     'connected components',
     'clustering coefficient',
     'density',
     'flow_hierarchy'])
    nodes = len(G.nodes())
    edges = len(G.edges())
    cc = len(list(nx.connected_components(G.to_undirected())))
    try:
        cc = nx.average_clustering(G.to_undirected())
    except:
        cc = None

    try:
        dx = nx.density(G)
    except:
        dx = None

    clustering = None
    if labels is not None:
        number_of_classes = labels.shape[1]
    else:
        number_of_classes = None
    mean_degree = np.mean(nx.degree(G).values())
    diameter = nx.diameter(G)
    flow_hierarchy = nx.flow_hierarchy(G)
    point = {'Name':name, 
     'classes':number_of_classes, 
     'nodes':nodes, 
     'edges':edges, 
     'diameter':diameter, 
     'degree':mean_degree, 
     'flow hierarchy':flow_hierarchy, 
     'connected components':cc, 
     'clustering coefficient':clustering, 
     'density':dx}
    rframe = rframe.append(point, ignore_index=True)
    return rframe