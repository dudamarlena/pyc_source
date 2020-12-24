# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/feynman/tests/test_v2_5_double.py
# Compiled at: 2018-05-31 10:24:13
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from ..diagrams import Diagram

@image_comparison(baseline_images=['double'], extensions=[
 'png'])
def test_double():
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    dia = Diagram(ax)
    v1 = dia.vertex(xy=(0.2, 0.5))
    v2 = dia.vertex(xy=(0.8, 0.5))
    l1 = dia.line(v1, v2, style='double linear', arrow=True, arrow_param={'linewidth': 2, 'width': 0.035})
    v3 = dia.vertex(xy=(0.2, 0.3))
    v4 = dia.vertex(xy=(0.8, 0.3))
    l2 = dia.line(v3, v4, style='linear double wiggly')
    v5 = dia.vertex(xy=(0.2, 0.1))
    v6 = dia.vertex(xy=(0.8, 0.1))
    l3 = dia.line(v5, v6, style='linear double loopy')
    l4 = dia.line(v1, v2, style='elliptic double wiggly')
    dia.plot()