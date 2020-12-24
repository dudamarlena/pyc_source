# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/visualization/plots.py
# Compiled at: 2019-06-11 07:56:19
# Size of source mod 2**32: 1271 bytes
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import pandas as pd

def UMAP_plot(X, Y, title='UMAP projection', fontsize=24, output='UMAPproj.png'):
    reducer = umap.UMAP(n_neighbors=5, min_dist=0.2)
    embedding = reducer.fit_transform(X)
    fig, ax = plt.subplots()
    ax.scatter((embedding[:, 0]), (embedding[:, 1]), c=[sns.color_palette()[y] for y in np.array(Y)])
    fig.gca().set_aspect('equal', 'datalim')
    ax.set_title(title)
    fig.savefig(output)


def plot(X, Y, labels, title='plot', fontsize=24, output='proj.png', true_false=False):
    fig, ax = plt.subplots()
    if true_false:
        x_true = []
        y_true = []
        x_false = []
        y_false = []
        for x, y, l in zip(X, Y, labels):
            if l:
                x_true.append(x)
                y_true.append(y)
            else:
                x_false.append(x)
                y_false.append(y)

        ax.scatter(x_true, y_true, c='g')
        ax.scatter(x_false, y_false, c='r')
    else:
        colors = cm.nipy_spectral(labels.astype(float) / (max(labels) + 1))
        ax.scatter(X, Y, c=colors)
    ax.set_title(title)
    fig.savefig(output)