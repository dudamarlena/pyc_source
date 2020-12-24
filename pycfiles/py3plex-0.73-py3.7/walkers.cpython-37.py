# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/general/walkers.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1738 bytes
import networkx as nx, numpy as np, random, itertools

def __random_number_set_generator(number):
    choices = np.random.rand(number)
    for x in choices:
        yield x


def general_random_walk(G, start_node, iterations=1000, teleportation_prob=0):
    random_number_generator = __random_number_set_generator(int(1000000.0))
    x = 0
    trace = []
    while x < iterations:
        neighbors = list(G.neighbors(start_node))
        num_neighbors = len(neighbors)
        probabilities = np.array(list(itertools.islice(random_number_generator, num_neighbors + 1)))
        teleport = probabilities[(-1)]
        if teleport > 1 - teleportation_prob:
            probabilities = np.array(list(itertools.islice(random_number_generator, len(trace))))
            ind = np.unravel_index(np.argmax(probabilities, axis=None), probabilities.shape)
            new_pivot = trace[ind[0]]
            start_node = new_pivot
            continue
        probabilities = probabilities[0:num_neighbors]
        ind = np.unravel_index(np.argmax(probabilities, axis=None), probabilities.shape)
        new_pivot = neighbors[ind[0]]
        trace.append(new_pivot)
        start_node = new_pivot
        x += 1

    return trace


def layer_specific_random_walk(G, start_node, iterations=1000):
    pass


if __name__ == '__main__':
    graph = nx.erdos_renyi_graph(1000, 0.01)
    print(nx.info(graph))
    trace = general_random_walk(graph, 5)
    print(trace)