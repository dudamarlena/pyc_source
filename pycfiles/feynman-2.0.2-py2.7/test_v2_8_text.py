# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/feynman/tests/test_v2_8_text.py
# Compiled at: 2018-05-31 10:24:20
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from ..diagrams import Diagram

@image_comparison(baseline_images=['text'], extensions=[
 'png'])
def test_text():
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    D1 = Diagram(ax)
    v1 = D1.vertex(xy=(0.2, 0.2), marker='')
    v2 = D1.vertex(xy=(0.4, 0.2))
    v3 = D1.vertex(xy=(0.6, 0.2))
    v4 = D1.vertex(xy=(0.8, 0.2), marker='')
    v1.text('1', x=-0.03, y=0.02)
    v2.text('2', x=-0.03, y=0.02)
    v3.text('3', x=0.01, y=0.02)
    v4.text('4', x=0.01, y=0.02)
    D1.line(v1, v2, arrow=True)
    O = D1.operator([v2, v3])
    O.text('S')
    D1.line(v3, v4, stroke='double', arrow=True)
    D1.plot()
    D2 = Diagram(ax)
    v1 = D2.vertex(xy=(0.1, 0.5), marker='')
    v2 = D2.vertex(xy=(0.3, 0.5))
    v3 = D2.vertex(xy=(0.7, 0.5))
    v4 = D2.vertex(xy=(0.9, 0.5), marker='')
    l12 = D2.line(v1, v2, arrow=True)
    w23 = D2.line(v2, v3, shape='elliptic', flavour='loopy', nloops=18)
    l23 = D2.line(v2, v3, arrow=True)
    l34 = D2.line(v3, v4, arrow=True)
    l12.text('p', t=0.5, y=-0.05, fontsize=18)
    w23.text('q', t=0.48, y=-0.05, fontsize=18)
    l23.text('p-q', t=0.35, y=-0.06, fontsize=18)
    l34.text('p', t=0.5, y=-0.05, fontsize=18)
    D2.plot()