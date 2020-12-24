# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/feynman/tests/test_v2_7_ellipse.py
# Compiled at: 2018-05-31 10:24:18
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from ..diagrams import Diagram

@image_comparison(baseline_images=['ellipse'], extensions=[
 'png'])
def test_ellipse():
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
    D1.line(v1, v2, arrow=True)
    O = D1.operator([v2, v3])
    O.text('S')
    D1.line(v3, v4, stroke='double', arrow=True)
    D1.plot()
    D2 = Diagram(ax)
    v1 = D2.vertex(xy=(0.2, 0.4), marker='')
    v2 = D2.vertex(xy=(0.4, 0.5))
    v3 = D2.vertex(xy=(0.6, 0.6))
    v4 = D2.vertex(xy=(0.8, 0.7), marker='')
    D2.line(v1, v2, arrow=True)
    D2.operator([v2, v3], c=1.5)
    D2.line(v3, v4, flavour='wiggly', nwiggles=2)
    D2.plot()