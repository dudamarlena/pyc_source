# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/plotting/interactive/annotators.py
# Compiled at: 2013-04-04 09:40:18
"""
Created on Jul 14, 2011

@author: jonathanfriedman
"""
import pylab
from numpy import abs, array, asarray, cumsum, nonzero, arange, random, shape
from PlotClicker import PlotClicker

class BaseAnnotator(PlotClicker):
    """
    Toggle draw of coordinates and annotation with click.
    """

    def __init__(self, xdata, ydata, **kwargs):
        PlotClicker.__init__(self, xdata, ydata, **kwargs)
        self.drawnAnnotations = {}
        self.write = kwargs.get('write', True)
        self.draw = kwargs.get('draw', False)
        self.title = kwargs.get('title', True)
        text_kwargs = kwargs.get('text_kwargs', {})
        text_kwargs.setdefault('ha', 'center')
        self.text_kwargs = text_kwargs


class Annotator(BaseAnnotator):
    """
    Toggle draw of coordinates and annotation with click.
    """

    def __init__(self, xdata, ydata, annotes, **kwargs):
        BaseAnnotator.__init__(self, xdata, ydata, **kwargs)
        self.annotes = annotes

    def _act(self, clickX, clickY):
        closest = self._closest2event(clickX, clickY)
        (i, x, y, d) = closest
        if abs(x - clickX) < self.xtol and abs(y - clickY) < self.ytol:
            annote = self.make_annote(i, x, y)
            self._annotate(x, y, annote)
        elif self.title:
            pylab.title('Not a data point.')
            pylab.draw()

    def _annotate(self, x, y, annote):
        """ Draw the annotation on the plot and/or write it to the screen."""
        axis = self.axis
        if self.write:
            print annote
        if self.title:
            pylab.title(annote)
            pylab.draw()
        if self.draw:
            if (
             x, y) in self.drawnAnnotations:
                markers = self.drawnAnnotations[(x, y)]
                for m in markers:
                    m.set_visible(not m.get_visible())

                self.axis.figure.canvas.draw()
            else:
                t = axis.text(x, y, annote, **self.text_kwargs)
                m = axis.scatter([x], [y], marker='d', c='r', zorder=100)
                self.drawnAnnotations[(x, y)] = (t, m)
                self.axis.figure.canvas.draw()

    def make_annote(self, i, x, y):
        a = self.annotes[i]
        annote = '(%3.2f, %3.2f) - %s' % (x, y, a)
        return annote


class XYAnnotator(BaseAnnotator):
    """
    Toggle draw of coordinates and annotation with click.
    """

    def __init__(self, xdata, ydata, xannotes=None, yannotes=None, **kwargs):
        BaseAnnotator.__init__(self, xdata, ydata, **kwargs)
        self.xdata = asarray(xdata)
        self.ydata = asarray(ydata)
        self.xannotes = xannotes
        self.yannotes = yannotes

    def _closest2event(self, clickX, clickY, axis):
        """ Get the index and data point that's closest to the mouse event."""
        if axis == 'x':
            click = clickX
            data = self.xdata
        elif axis == 'y':
            click = clickY
            data = self.ydata
        dist = abs(data - click)
        i = dist.argmin()
        return (i, data[i], dist[i])

    def _act(self, clickX, clickY):
        out = self.make_annote(clickX, clickY)
        if out is not None:
            (x, y, annote) = out
            self._annotate(x, y, annote)
        elif self.title:
            pylab.title('Not a data point.')
            pylab.draw()
        return

    def _annotate(self, x, y, annote):
        """ Draw the annotation on the plot and/or write it to the screen."""
        axis = self.axis
        if self.write:
            print annote
        if self.title:
            pylab.title(annote)
            pylab.draw()
        if self.draw:
            if (
             x, y) in self.drawnAnnotations:
                markers = self.drawnAnnotations[(x, y)]
                for m in markers:
                    m.set_visible(not m.get_visible())

                self.axis.figure.canvas.draw()
            else:
                t = axis.text(x, y, annote, **self.text_kwargs)
                m = axis.scatter([x], [y], marker='d', c='r', zorder=100)
                self.drawnAnnotations[(x, y)] = (t, m)
                self.axis.figure.canvas.draw()

    def make_annote(self, clickX, clickY):
        """
        Find the annotations for click coordinates
        """
        print clickX, clickY
        annote = ''
        (i, x, d) = self._closest2event(clickX, clickY, 'x')
        if abs(x - clickX) < self.xtol:
            if self.xannotes is not None:
                xannote = str(self.xannotes[i])
        else:
            return
        (i, y, d) = self._closest2event(clickX, clickY, 'y')
        if abs(y - clickY) < self.ytol:
            if self.yannotes is not None:
                yannote = self.yannotes[i]
        else:
            return
        if self.xannotes is not None:
            annote += xannote
        if self.yannotes is not None:
            if annote:
                annote += ' ; '
            annote += str(yannote)
        return (
         x, y, annote)


class MultibarAnnotator(XYAnnotator):
    """
    Object for annotating multibar plots.
    """

    def __init__(self, xdata, ydata, xannotes=None, yannotes=None, style='stacked', **kwargs):
        """
        Constructor
        """
        XYAnnotator.__init__(self, xdata, ydata, xannotes, yannotes, **kwargs)
        self.axis.autoscale(enable=False)
        self.style = style

    def make_annote(self, clickX, clickY):
        """
        Find the annotations for click coordinates
        """
        style = self.style
        yannote = None
        xannote = None
        if style == 'stacked':
            (i, x, d) = self._closest2event(clickX, clickY, axis='x')
            if abs(x - clickX) < self.xtol:
                xannote = self.xannotes[i]
            ycum = cumsum(self.ydata[i])
            if clickY > ycum[(-1)] + self.ytol:
                pass
            else:
                if clickY > ycum[(-1)]:
                    j = len(ycum) - 1
                else:
                    j = nonzero(ycum - clickY > 0)[0][0]
                if j > 0:
                    y = ycum[(j - 1)] + (ycum[j] - ycum[(j - 1)]) / 2.0
                else:
                    y = ycum[j] / 2.0
                yannote = self.yannotes[j]
        elif style == 'grouped':
            raise ValueError, 'Grouped style not yet supported'
        else:
            raise ValueError('Unknown style %s' % style)
        if xannote is not None and yannote is not None:
            annote = xannote + ';  ' + yannote
            return (
             x, y, annote)
        else:
            return
            return


class StackedAnnotator(MultibarAnnotator):

    def __init__(self, xdata, ydata, xannotes=None, yannotes=None, style='stacked', **kwargs):
        """
        Constructor
        """
        MultibarAnnotator.__init__(self, xdata, ydata, xannotes, yannotes, style=style, **kwargs)
        self.ydata = self.ydata.T
        self.data = zip(self.xdata, self.ydata)


class HeatmapAnnotator(XYAnnotator):

    def __init__(self, rlocs, clocs, rannotes=None, cannotes=None, origin='upper', **kwargs):
        """
        Constructor
        """
        if rannotes is not None:
            if origin is 'lower':
                rannotes = rannotes[::-1]
        XYAnnotator.__init__(self, clocs, rlocs, cannotes, rannotes, **kwargs)
        self.axis.autoscale(enable=False)
        return


if __name__ == '__main__':
    pass