# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/visualization/embedding_visualization/embedding_visualization.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1165 bytes
from sklearn.manifold import TSNE
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from plotnine import *

def visualize_embedding(multinet, labels=None, verbose=True):
    embedding = multinet.embedding
    X = embedding[0]
    indices = embedding[1]
    if verbose:
        print('------ Starting embedding visualization -------')
    elif labels:
        label_vector = [labels[x] for x in indices]
        X_embedded = TSNE(n_components=2).fit_transform(X)
        dfr = pd.DataFrame(X_embedded, columns=['dim1', 'dim2'])
        dfr['labels'] = label_vector
        print(dfr.head())
        gx = ggplot(dfr, aes('dim1', 'dim2', color='labels')) + geom_point(size=0.5) + theme_bw()
        gx.draw()
        plt.show()
    else:
        X_embedded = TSNE(n_components=2).fit_transform(X)
        dfr = pd.DataFrame(X_embedded, columns=['dim1', 'dim2'])
        print(dfr.head())
        gx = ggplot(dfr, aes('dim1', 'dim2')) + geom_point(size=0.5) + theme_bw()
        gx.draw()
        plt.show()