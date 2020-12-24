# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/feynman/tests/test_v2_2_wiggly.py
# Compiled at: 2018-05-31 10:24:06
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from ..diagrams import Diagram

@image_comparison(baseline_images=['wiggly'], extensions=[
 'png'])
def test_wiggly():
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    D = Diagram(ax)
    v1 = D.vertex(xy=(0.2, 0.5))
    v2 = D.vertex(xy=(0.8, 0.5))
    l1 = D.line(v1, v2, arrow=True)
    l2 = D.line(v1, v2, shape='elliptic', flavour='wiggly')
    D.plot()