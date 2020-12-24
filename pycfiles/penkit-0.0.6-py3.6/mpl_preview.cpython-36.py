# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/penkit/mpl_preview.py
# Compiled at: 2017-12-10 17:14:10
# Size of source mod 2**32: 1023 bytes
"""Preview plots with matplotlib.

Alternative to the ``preview`` module for non-Jupyter environments.
"""
import matplotlib.pyplot as plt

def draw_layer(ax, layer):
    """Draws a layer on the given matplotlib axis.

    Args:
        ax (axis): the matplotlib axis to draw on
        layer (layer): the layers to plot
    """
    ax.set_aspect('equal', 'datalim')
    (ax.plot)(*layer)
    ax.axis('off')


def draw_plot(ax, plot):
    """Draws a plot on the given matplotlib axis.

    Args:
        ax (axis): the matplotlib axis to draw on
        plot (list): the layers to plot
    """
    for layer in plot:
        show_layer(ax, layer)


def show_layer(layer):
    """Shortcut for ``show_plot`` when only one layer is needed.

    Args:
        layer (layer): the layer to plot
    """
    show_plot([layer])


def show_plot(plot):
    """Draws a preview of the given plot with matplotlib.

    Args:
        plot (list): the plot as a list of layers
    """
    fig, ax = plt.subplots()
    draw_plot(ax, plot)