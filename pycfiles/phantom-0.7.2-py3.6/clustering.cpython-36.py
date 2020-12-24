# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\phantom\clustering.py
# Compiled at: 2019-02-15 09:35:28
# Size of source mod 2**32: 1182 bytes
"""
Clustering functions written specifically for the project.

"""
import numpy as np
from pprint import pprint

def distance(x, y):
    return np.linalg.norm(x - y)


def bruno(array, threshold=0.5):
    labeled_array = np.zeros(array.shape[0])
    clusters = [[array[0]]]
    centroids = [[array[0]]]
    c_history = [centroids[:]]
    for i, e in enumerate(array[1:], 1):
        new_centroids = [np.mean((c + [e]), axis=0) for c in clusters]
        distances = [distance(c, e) for c in new_centroids]
        index = np.argmin(distances)
        dist = distances[index]
        if dist <= threshold:
            clusters[index].append(e)
            centroids[index] = new_centroids[index]
            labeled_array[i] = index
        else:
            new_cluster = len(clusters)
            clusters.append([e])
            centroids.append([e])
            labeled_array[i] = new_cluster
        c_history.append(centroids[:])

    return (
     labeled_array, centroids, c_history)