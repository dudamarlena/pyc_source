# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webplotlib/urls.py
# Compiled at: 2011-05-12 17:38:43
from django.conf.urls.defaults import *
urlpatterns = patterns('webplotlib.views', url('^ts_plot/foo.png$', 'show_ts_plot_png'), url('^bar_plot/bar.png$', 'show_bar_plot_png'))