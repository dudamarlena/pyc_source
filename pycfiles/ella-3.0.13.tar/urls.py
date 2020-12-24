# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/urls.py
# Compiled at: 2013-07-24 08:14:41
try:
    from django.conf.urls import patterns, include
except ImportError:
    from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('', (
 '^', include('ella.core.urls')))