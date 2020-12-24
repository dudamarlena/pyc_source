# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/enlp/visualisation/word_vectors.py
# Compiled at: 2019-11-27 15:57:30
# Size of source mod 2**32: 1405 bytes
"""
Contains functions for visualising word vectors
"""
from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
import enlp.understanding.vectors as vts

def similar_words(model, word, n=25, ax=None):
    """ Create a plot of similar words based off their word vectors

    Parameters
    ----------
    model : :obj:`gensim.model`
        Trained word vector model
    word : :obj:`str`
        word to find most similar vectors, note it must be within vocabulary
    n  : :obj:`int`
        Number of similar words to return.
    ax : :obj:`matplotlib.axes.Axis`
        Axis object for figure

    Returns
    -------
    fig : :obj:`matplotlib.figure.Figure`
        Figure object line plot of word counts
    ax : :obj:`matplotlib.axes.Axis`
        Axis object for figure

    """
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    else:
        fig = None
    sim_words = [sw[0] for sw in vts.similar_words(model, word, n=n)]
    vocab = sim_words + [word]
    vectors = model[vocab]
    tsne = TSNE(n_components=2)
    X_tsne = tsne.fit_transform(vectors)
    df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
    ax.scatter(df['x'], df['y'])
    for word, pos in df.iterrows():
        ax.annotate(word, pos)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    return (
     fig, ax)