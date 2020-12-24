# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider/config.py
# Compiled at: 2006-03-30 03:06:13
path('/static')
static_filter.on = True
static_filter.dir = absfile('spider', 'static')
path('/favicon.ico')
static_filter.on = True
static_filter.file = absfile('spider', 'static/images/favicon.ico')