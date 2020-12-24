# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/chart.py
# Compiled at: 2020-01-18 11:47:38
from __future__ import absolute_import
from odf.namespaces import CHARTNS
from odf.element import Element

def Axis(**args):
    return Element(qname=(CHARTNS, 'axis'), **args)


def Categories(**args):
    return Element(qname=(CHARTNS, 'categories'), **args)


def Chart(**args):
    return Element(qname=(CHARTNS, 'chart'), **args)


def DataLabel(**args):
    return Element(qname=(CHARTNS, 'data-label'), **args)


def DataPoint(**args):
    return Element(qname=(CHARTNS, 'data-point'), **args)


def Domain(**args):
    return Element(qname=(CHARTNS, 'domain'), **args)


def Equation(**args):
    return Element(qname=(CHARTNS, 'equation'), **args)


def ErrorIndicator(**args):
    return Element(qname=(CHARTNS, 'error-indicator'), **args)


def Floor(**args):
    return Element(qname=(CHARTNS, 'floor'), **args)


def Footer(**args):
    return Element(qname=(CHARTNS, 'footer'), **args)


def Grid(**args):
    return Element(qname=(CHARTNS, 'grid'), **args)


def LabelSeparator(**args):
    return Element(qname=(CHARTNS, 'label-separator'), **args)


def Legend(**args):
    return Element(qname=(CHARTNS, 'legend'), **args)


def MeanValue(**args):
    return Element(qname=(CHARTNS, 'mean-value'), **args)


def PlotArea(**args):
    return Element(qname=(CHARTNS, 'plot-area'), **args)


def RegressionCurve(**args):
    return Element(qname=(CHARTNS, 'regression-curve'), **args)


def Series(**args):
    return Element(qname=(CHARTNS, 'series'), **args)


def StockGainMarker(**args):
    return Element(qname=(CHARTNS, 'stock-gain-marker'), **args)


def StockLossMarker(**args):
    return Element(qname=(CHARTNS, 'stock-loss-marker'), **args)


def StockRangeLine(**args):
    return Element(qname=(CHARTNS, 'stock-range-line'), **args)


def Subtitle(**args):
    return Element(qname=(CHARTNS, 'subtitle'), **args)


def SymbolImage(**args):
    return Element(qname=(CHARTNS, 'symbol-image'), **args)


def Title(**args):
    return Element(qname=(CHARTNS, 'title'), **args)


def Wall(**args):
    return Element(qname=(CHARTNS, 'wall'), **args)