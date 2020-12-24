# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/ReportRenderHtml.py
# Compiled at: 2015-05-06 05:03:08
"""Choose the best html rendering

$Id: ReportRenderHtml.py 53544 2009-03-09 16:28:58Z tlazar $
"""
try:
    from ReportRenderHtmlGnuPlot import RenderHtmlGnuPlot as RenderHtml
except ImportError:
    from ReportRenderHtmlBase import RenderHtmlBase as RenderHtml

from ReportRenderHtmlGnuPlot import RenderHtmlGnuPlot as RenderHtml