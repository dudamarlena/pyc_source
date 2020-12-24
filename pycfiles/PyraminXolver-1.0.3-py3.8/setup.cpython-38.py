# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyraminxolver\setup.py
# Compiled at: 2019-10-26 14:37:05
# Size of source mod 2**32: 1191 bytes
from collections import deque
import pickle
from . import Pyraminx, PYRAMINX_CASE_PATH
from multiprocessing import Pool, cpu_count

def setup():
    graph = create_graph()
    with open(PYRAMINX_CASE_PATH, 'wb') as (f):
        pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)


def create_graph():
    with Pool(cpu_count()) as (p):
        graph = p.map(explore_node, [x for x in range(933120)])
    graph = generate_depths(graph)
    return graph


def explore_node(node):
    state = Pyraminx.id_to_state(node)
    node_values = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    for i in range(1, 9):
        transformation = Pyraminx.move_transformations[(i - 1)]
        new_state = Pyraminx.apply_move(state, transformation)
        new_id = Pyraminx.state_to_id(new_state)
        node_values[i] = new_id
    else:
        return node_values


def generate_depths(graph):
    queue = deque()
    graph[0][0] = 0
    queue.append(0)
    while queue:
        i = queue.popleft()
        depth = graph[i][0]
        for edge in graph[i][1:]:
            if graph[edge][0] == -1:
                graph[edge][0] = depth + 1
                queue.append(edge)

    return graph


if __name__ == '__main__':
    setup()