# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/plot_help.py
# Compiled at: 2007-04-18 06:57:54
from pylab import *

class Series:
    __module__ = __name__

    def __init__(self, xvalues, yvalues, label=''):
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.label = label


def seriesMaker(xvalues, function, label=''):
    yvalues = []
    for xval in xvalues:
        yvalues.append(function(xval))

    return Series(xvalues, yvalues, label)


def plotAssistant(listOfSeries, caption='', xtitle='', ytitle=''):
    markers = ['+', ',', 'x', 'o', '.', 's', 'v', 's', '>', '<', '^']
    plotArgs = []
    if len(listOfSeries) >= 7:
        raise Exception('Cannot handle more than seven series and ' + len(listOfSeries) + ' series were supplied')
    for ii in range(len(listOfSeries)):
        (line,) = plot(listOfSeries[ii].xvalues, listOfSeries[ii].yvalues)
        line.set_marker(markers[ii])
        line.set_label(listOfSeries[ii].label)

    title(caption)
    legend(loc='upper right')
    xlabel(xtitle)
    ylabel(ytitle)


if __name__ == '__main__':
    xvals = [
     1, 2, 3]
    yvals = [ x ** 2 for x in xvals ]
    series1 = Series(xvals, yvals)