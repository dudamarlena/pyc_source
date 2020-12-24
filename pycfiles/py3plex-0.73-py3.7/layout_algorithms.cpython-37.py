# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/visualization/layout_algorithms.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 2722 bytes
import networkx as nx, numpy as np, itertools
try:
    from .fa2 import ForceAtlas2
    forceImport = True
    print('Imported BH algo')
except:
    forceImport = False

def compute_force_directed_layout(g, layout_parameters=None, verbose=True, gravity=0.2, strongGravityMode=False, barnesHutTheta=1.2, edgeWeightInfluence=1, scalingRatio=2.0, forceImport=True):
    if forceImport:
        try:
            forceatlas2 = ForceAtlas2(outboundAttractionDistribution=False,
              linLogMode=False,
              adjustSizes=False,
              edgeWeightInfluence=edgeWeightInfluence,
              jitterTolerance=1.0,
              barnesHutOptimize=True,
              barnesHutTheta=barnesHutTheta,
              multiThreaded=False,
              scalingRatio=scalingRatio,
              strongGravityMode=False,
              gravity=gravity,
              verbose=verbose)
            if layout_parameters != None:
                print('Using custom init positions!')
                pos = (forceatlas2.forceatlas2_networkx_layout)(g, **layout_parameters)
            else:
                pos = forceatlas2.forceatlas2_networkx_layout(g)
            norm = np.max([np.abs(x) for x in itertools.chain(zip(*pos.values()))])
            pos_pairs = [np.array([a / norm, b / norm]) for a, b in pos.values()]
            pos = dict(zip(pos.keys(), pos_pairs))
        except Exception as e:
            try:
                print(e)
                if layout_parameters is not None:
                    pos = (nx.spring_layout)(g, **layout_parameters)
                else:
                    pos = nx.spring_layout(g)
                print('Using standard layout algorithm, fa2 not present on the system.')
            finally:
                e = None
                del e

    else:
        if layout_parameters is not None:
            pos = (nx.spring_layout)(g, **layout_parameters)
        else:
            pos = nx.spring_layout(g)
        print('Using standard layout algorithm, fa2 not present on the system.')
    return pos


def compute_random_layout(g):
    coordinates = tuple(np.random.rand(1, 2))
    pos = {n:np.array(tuple(np.random.rand(1, 2).tolist()[0])) for n in g.nodes()}
    return pos


if __name__ == '__main__':
    G = nx.gaussian_random_partition_graph(1000, 10, 10, 0.25, 0.1)
    print(nx.info(G))
    compute_force_directed_layout(G)
    print('Finished..')