# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/matplotlib_subsets/__init__.py
# Compiled at: 2013-12-04 12:48:04
"""
Subset diagram plotting routines.

Copyright 2013, Johannes Buchner.

Licensed under MIT license.
"""
import numpy, warnings, string, matplotlib.pyplot as plt, matplotlib.transforms as mtransforms
from matplotlib.patches import FancyBboxPatch
import itertools, scipy.stats
default_attrs = [ dict(ec=c, fc='None', alpha=0.7) for c in ['black', 'blue', 'red', 'green', 'magenta'] ]
default_attrs = itertools.cycle(default_attrs)

def plot_box(bbox, label='', attrs={}):
    (xmin, ymin), (xmax, ymax) = bbox.get_points()
    if attrs is None:
        attrs = default_attrs.next()
        print 'picked attrs:', attrs
    ax = plt.gca()
    print 'plotting %s at' % label, ((xmin, ymin), (xmax, ymax))
    p_fancy = FancyBboxPatch((xmin, ymin), (xmax - xmin), (ymax - ymin), boxstyle='round,pad=0.0, rounding_size=0.02', **attrs)
    ax.add_patch(p_fancy)
    ax.text(xmin + 0.01, ymax - 0.01, label, horizontalalignment='left', verticalalignment='top')
    return


def nodesets_rectangles((node, children), bbox):
    nodesize, nodelabel, nodeattrs = node
    nchildren = len(children)
    print 'node', node
    print '   has %d children:' % nchildren
    for i, c in enumerate(children):
        print '     %i: %s' % (i, c)

    (xmin0, ymin0), (xmax0, ymax0) = bbox.get_points()
    deltay = ymax0 - ymin0
    deltax = xmax0 - xmin0
    if nchildren > 0:
        nsizechildren = sum([ size for (size, label, attrs), grandchildren in children ])
        empty = 1 - nsizechildren * 1.0 / nodesize
        fbuffer = empty ** 0.5
        yratio = deltay * (nsizechildren * 1.0 / nodesize) / deltax
        print 'yratio %s:' % str(node), yratio
        print 'deltax, deltay:', deltax, deltay
    for child, grandchildren in children:
        (xmin, ymin), (xmax, ymax) = bbox.get_points()
        size, label, attrs = child
        arearatio = size * 1.0 / nodesize
        print 'arearatio of child:', arearatio
        if arearatio == 0:
            continue
        if nchildren == 1:
            print 'single subset: arearatio', arearatio
            a, b = (10, 1)
            rv = scipy.stats.beta(a, b)
            fx = rv.ppf(arearatio)
            fy = arearatio / fx
            print 'fx, fy:', fx, fy
            ypad = min(fy * 0.02, 1 - fy)
            xpad = min(fx * 0.02, 1 - fx)
            ymax = ymax - deltay * (1 - (fy + ypad))
            xmin = xmin + deltax * (1 - (fx + xpad))
            ymin = ymin + deltay * ypad
            xmax = xmax - deltax * xpad
        elif yratio > 0.4:
            print 'splitting in y: starting box', ((xmin0, ymin0), (xmax0, ymax0))
            ymin, ymax = ymin0, ymin0 + deltay * arearatio - 1.0 * deltay * fbuffer / 40
            ymax0, ymin0 = ymax0, ymin0 + deltay * arearatio + 1.0 * deltay * fbuffer / 40
            print 'splitting in y: child box', ((xmin, ymin), (xmax, ymax))
            print 'splitting in y: remaining box', ((xmin0, ymin0), (xmax0, ymax0))
        else:
            print 'splitting in x: starting box', ((xmin0, ymin0), (xmax0, ymax0))
            xmin, xmax = xmax0 - deltax * arearatio + deltax * fbuffer / 40, xmax0
            xmax0, xmin0 = xmax0 - deltax * arearatio - deltax * fbuffer / 40, xmin0
            print 'splitting in x: child box', ((xmin, ymin), (xmax, ymax))
            print 'splitting in x: remaining box', ((xmin0, ymin0), (xmax0, ymax0))
        childbox = mtransforms.Bbox(((xmin, ymin), (xmax, ymax)))
        nodesets_rectangles((child, grandchildren), childbox)
        plot_box(bbox=childbox, attrs=attrs, label=label)


def treesets_rectangles(tree):
    (xmin, xmax), (ymin, ymax) = (0, 1), (0, 1)
    superset = None
    ax = plt.gca()
    ax.set_aspect(1.0)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis('off')
    root, children = tree
    size, label, attrs = root
    assert size > 0
    rootbox = mtransforms.Bbox([[xmin, ymin], [xmax, ymax]])
    nodesets_rectangles((root, children), rootbox)
    plot_box(bbox=rootbox, attrs=attrs, label=label)
    return


def nestedsets_rectangles(setsizes, labels=None, attrs=None):
    nsets = len(setsizes)
    if labels is None:
        labels = list(string.ascii_uppercase)[:nsets]
    if attrs is None:
        attrs = [ default_attrs.next() for i in range(nsets) ]
    tree = []
    for node in list(zip(setsizes, labels, attrs))[::-1]:
        tree = [[node, tree]]

    treesets_rectangles(tree[0])
    return