# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaplot.py
# Compiled at: 2014-08-21 22:30:04


def iaplot(Ylist, Xlist=[], arrows_list=[], text_list=[], ylabel='y', xlabel='x', title='', colors='rgbmyc', shapes='------', axis='tight', fig_size=[], face_color='w'):
    import numpy as np, matplotlib.pyplot as plt, ia636
    if isinstance(Ylist, np.ndarray):
        Ylist = [
         Ylist]
    if Xlist == []:
        Xlist = [ np.arange(len(i)) for i in Ylist ]
    if isinstance(Xlist, np.ndarray):
        Xlist = [
         Xlist]
    if fig_size == []:
        fig = plt.figure(facecolor=face_color)
    else:
        fig = plt.figure(figsize=fig_size, facecolor=face_color)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    for x, y, c, s in zip(Xlist, Ylist, colors[:len(Xlist)], shapes[:len(Xlist)]):
        plt.plot(x, y, c + s, markersize=9)

    for arrow in arrows_list:
        plt.arrow(arrow[0], arrow[1], arrow[2], arrow[3], fc='k', ec='k', head_width=0.15, head_length=0.2)

    for text in text_list:
        plt.annotate(text[0], xy=(text[1], text[2]), xycoords='data', xytext=(text[1], text[2]), textcoords='data')

    plt.grid()
    plt.axis(axis)
    return ia636.iafig2img(fig)