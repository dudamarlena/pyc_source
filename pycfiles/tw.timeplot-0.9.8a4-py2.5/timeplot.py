# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tw/timeplot/timeplot.py
# Compiled at: 2009-05-07 20:44:55
from base import TimelineCSSLink, TimelineJSLink, JSLink

class timeplot_js(TimelineJSLink):
    basename = 'scripts/timeplot'
    javascript = []
    css = []


timeplot_js = timeplot_js()

class timeplot_api_js(TimelineJSLink):
    basename = 'timeplot-api'
    javascript = []
    css = []