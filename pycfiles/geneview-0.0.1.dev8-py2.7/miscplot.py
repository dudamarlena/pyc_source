# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/geneview/ext/miscplot.py
# Compiled at: 2016-02-14 08:28:41
from __future__ import division
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt

def palplot(pal, size=1):
    """Plot the values in a color palette as a horizontal array.

    Parameters
    ----------
    pal : sequence of matplotlib colors
        colors
    size :
        scaling factor for size of plot

    """
    n = len(pal)
    f, ax = plt.subplots(1, 1, figsize=(n * size, size))
    ax.imshow(np.arange(n).reshape(1, n), cmap=mpl.colors.ListedColormap(list(pal)), interpolation='nearest', aspect='auto')
    ax.set_xticks(np.arange(n) - 0.5)
    ax.set_yticks([-0.5, 0.5])
    ax.set_xticklabels([])
    ax.set_yticklabels([])


def puppyplot(grown_up=False):
    """Plot today's daily puppy. Only works in the IPython notebook."""
    from .six.moves.urllib.request import urlopen
    from IPython.display import HTML
    try:
        from bs4 import BeautifulSoup
        url = 'http://www.dailypuppy.com'
        if grown_up:
            url += '/dogs'
        html_doc = urlopen(url)
        soup = BeautifulSoup(html_doc, 'lxml')
        puppy = soup.find('div', {'class': 'daily_puppy'})
        return HTML(str(puppy.img))
    except ImportError:
        html = '<img src="http://cdn-www.dailypuppy.com/media/dogs/77165_20151221_023650412_iOS.jpg_w750.jpg" style="width:450px;"/>'
        return HTML(html)