# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tw/timeline/timeline.py
# Compiled at: 2009-02-12 15:12:06
from base import TimelineCSSLink, TimelineJSLink, JSLink

class timeline_api_js(TimelineJSLink):
    basename = 'timeline-api'
    javascript = []
    css = []


demo_js = JSLink(modname=__name__, filename='static/2.2.0/demo.js')