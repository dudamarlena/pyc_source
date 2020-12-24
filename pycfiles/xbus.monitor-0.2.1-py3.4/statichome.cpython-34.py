# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/statichome.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 173 bytes
from pyramid.static import static_view
static_view = static_view('xbus.monitor:static/monitor_js/sources', use_subpath=True)