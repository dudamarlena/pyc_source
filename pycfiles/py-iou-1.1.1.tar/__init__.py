# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dheepakkrishnamurthy/Documents/GitRepos/iou/iou/data/__init__.py
# Compiled at: 2016-03-20 05:30:33
import networkx as nx, pandas as pd

def get_transactions_from_file(f):
    df = pd.read_csv(f)
    array = df.values
    people = df.columns[3:].values
    return (
     array, people)


def create_graph(array, people):
    G = nx.MultiDiGraph()
    for person_name in people:
        if person_name is None:
            pass
        else:
            G.add_node(person_name)

    for row_number, row in enumerate(array):
        number_of_contributors = sum([ float(item) for item in row[3:] ])
        for i, item in enumerate(row[3:]):
            if item != '0':
                G.add_edge(people[i], row[2], owe=float(item) * float(row[1].strip('$')) / number_of_contributors)

    return G


def compress_edges(G):
    net_value = {}
    for node in G.nodes():
        net_value[node] = 0

    for edge in G.edges(data=True):
        net_value[edge[0]] -= edge[2]['owe']
        net_value[edge[1]] += edge[2]['owe']

    net_value = {key:-value for key, value in net_value.items()}
    return net_value