# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/legend.py
# Compiled at: 2016-09-29 12:46:03
from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import re, six

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {b'&': b'\\&', 
       b'%': b'\\%', 
       b'$': b'\\$', 
       b'#': b'\\#', 
       b'_': b'\\_', 
       b'{': b'\\{', 
       b'}': b'\\}', 
       b'~': b'\\textasciitilde{}', 
       b'^': b'\\^{}', 
       b'\\': b'\\textbackslash{}', 
       b'<': b'\\textless', 
       b'>': b'\\textgreater'}
    regex = re.compile((b'|').join(re.escape(six.text_type(key)) for key in sorted(conv.keys(), key=lambda item: -len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


def color_legend(color):
    return plt.Line2D([0], [0], color=color, linewidth=5)


def size_legend(size):
    return plt.Line2D([0], [0], color=b'black', marker=b'o', linestyle=b'None', markersize=size ** 0.5)


def alpha_legend(alpha):
    return plt.Line2D([0], [0], color=b'black', marker=b'o', linestyle=b'None', alpha=alpha)


def shape_legend(shape):
    return plt.Line2D([0], [0], color=b'black', marker=shape, linestyle=b'None')


def linetype_legend(linetype):
    return plt.Line2D([0], [0], color=b'black', linestyle=linetype)


def make_aesthetic_legend(aesthetic, value):
    if aesthetic == b'color':
        return color_legend(value)
    if aesthetic == b'fill':
        return color_legend(value)
    if aesthetic == b'size':
        return size_legend(value)
    if aesthetic == b'alpha':
        return alpha_legend(value)
    if aesthetic == b'shape':
        return shape_legend(value)
    if aesthetic == b'linetype':
        return linetype_legend(value)
    print(aesthetic + b' not found')


def make_legend(ax, legend_mapping):
    extra = Rectangle((0, 0), 0, 0, facecolor=b'w', fill=False, edgecolor=b'none', linewidth=0)
    items = []
    labels = []
    for aesthetic in [b'color', b'fill', b'shape', b'alpha', b'size', b'linetype']:
        if aesthetic in legend_mapping:
            items.append(extra)
            colname = legend_mapping[aesthetic][b'name']
            spacer = b'\n' if len(labels) > 0 else b''
            labels.append(spacer + colname)
            for key in sorted(legend_mapping[aesthetic][b'lookup'].keys()):
                value = legend_mapping[aesthetic][b'lookup'][key]
                legend_item = make_aesthetic_legend(aesthetic, value)
                items.append(legend_item)
                labels.append(key)

    legend = ax.legend(items, labels, loc=b'center left', bbox_to_anchor=(1.05, 0.5), fontsize=b'small', frameon=False)