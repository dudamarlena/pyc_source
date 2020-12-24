# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gratia/graphs/gratia_graphs.py
# Compiled at: 2008-01-21 15:26:02
from graphtool.graphs.graph import DBGraph, TimeGraph, SummarizePivotGroupGraph, SummarizePivotGraph
from graphtool.graphs.common_graphs import StackedBarGraph, BarGraph, CumulativeGraph, PieGraph, QualityMap
import types
from graphtool.graphs.graph import prefs
prefs['watermark'] = 'False'

class GratiaColors:
    __module__ = __name__


class GratiaStackedBar(GratiaColors, SummarizePivotGroupGraph, TimeGraph, StackedBarGraph):
    __module__ = __name__


class GratiaBar(GratiaColors, TimeGraph, BarGraph):
    __module__ = __name__


class GratiaCumulative(GratiaColors, SummarizePivotGroupGraph, CumulativeGraph):
    __module__ = __name__


class GratiaPie(GratiaColors, SummarizePivotGraph, TimeGraph, PieGraph):
    __module__ = __name__