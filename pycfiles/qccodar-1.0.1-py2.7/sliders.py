# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/qccodar/qcviz/sliders.py
# Compiled at: 2017-08-23 08:27:19
""" new classes of slider 
"""
import sys, matplotlib.widgets, numpy

class DiscreteSlider(matplotlib.widgets.Slider):
    """A matplotlib slider widget with discrete steps."""

    def __init__(self, *args, **kwargs):
        """Identical to Slider.__init__, except for the "increment" kwarg.
        "increment" specifies the step size that the slider will be discritized
        to."""
        self.inc = kwargs.pop('increment', 0.5)
        matplotlib.widgets.Slider.__init__(self, *args, **kwargs)

    def set_val(self, val):
        discrete_val = int(val / self.inc) * self.inc
        xy = self.poly.xy
        xy[2] = (discrete_val, 1)
        xy[3] = (discrete_val, 0)
        self.poly.xy = xy
        self.valtext.set_text(self.valfmt % discrete_val)
        if self.drawon:
            self.ax.figure.canvas.draw()
        self.val = val
        if not self.eventson:
            return
        for cid, func in self.observers.iteritems():
            func(discrete_val)


class IndexedSlider(matplotlib.widgets.Slider):
    """A matplotlib slider widget with discrete steps that index a list of values."""

    def __init__(self, *args, **kwargs):
        """Identical to Slider.__init__, except for the "seqvals" kwarg.
        "seqvals" specifies the sequence of values to be indexed by
        the slider.  The slider will be discritized so that self.val
        is an index to specific value in "seqvals".
        """
        seqvals = kwargs.pop('seqvals', range(1, 11))
        if type(seqvals) is type(numpy.array([])):
            self.seqvals = seqvals.tolist()
        elif type(seqvals) is type([]):
            self.seqvals = seqvals
        else:
            print 'Input param "seqvals" must be a list or numpy.array.'
        self.step = 1
        args = list(args)
        if len(args) <= 2:
            args.append(0)
            args.append(len(self.seqvals))
        elif len(args) == 4:
            args[2] = 0
            args[3] = len(self.seqvals)
        valinit = kwargs.pop('valinit', None)
        if not valinit:
            self.valinit = 0
        elif self.seqvals.count(valinit):
            self.valinit = self.seqvals.index(valinit)
        else:
            min = lambda x, y: x if x < y else y
            absdiff = map(lambda x: abs(x - valinit), seqvals)
            idx = absdiff.index(reduce(min, absdiff))
            seqvalinit = self.seqvals[idx]
            self.valinit = self.seqvals.index(seqvalinit)
        kwargs['valinit'] = self.valinit
        matplotlib.widgets.Slider.__init__(self, *args, **kwargs)
        self.valtext.set_text(self.valfmt % seqvals[self.valinit])
        return

    def set_val(self, val):
        discrete_val = int(val / self.step) * self.step
        xy = self.poly.xy
        xy[2] = (discrete_val, 1)
        xy[3] = (discrete_val, 0)
        self.poly.xy = xy
        self.valtext.set_text(self.valfmt % self.seqvals[discrete_val])
        if self.drawon:
            self.ax.figure.canvas.draw()
        self.val = val
        if not self.eventson:
            return
        for cid, func in self.observers.iteritems():
            func(discrete_val)


def _test():
    import matplotlib.pyplot as plt, matplotlib.pylab as pylab

    def discrete_slider_update(val):
        dot.set_xdata([val])
        dot.set_ydata([val])
        fig.canvas.draw()

    def indexed_slider_update(val):
        dot.set_xdata([val])
        dot.set_ydata([isbear.seqvals[val]])
        fig.canvas.draw()

    fig, ax = plt.subplots()
    seqvals = range(50, 0, -1)
    xseq = range(0, len(seqvals), 1)
    dsax = fig.add_axes([0.2, 0.2, 0.6, 0.03])
    dsbear = DiscreteSlider(dsax, 'Discrete', 0, 10, increment=1)
    dsbear.on_changed(discrete_slider_update)
    isax = fig.add_axes([0.2, 0.1, 0.6, 0.03])
    isbear = IndexedSlider(isax, 'Indexed', 50, 0, valinit=25.5, seqvals=seqvals)
    isbear.on_changed(indexed_slider_update)
    ax.plot(xseq, seqvals, 'ro')
    dot, = ax.plot(isbear.valinit, seqvals[isbear.valinit], 'bo', markersize=18)