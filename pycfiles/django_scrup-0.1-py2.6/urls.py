# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/scrup/urls.py
# Compiled at: 2010-03-08 16:45:09
from django.conf.urls.defaults import *
urlpatterns = patterns('scrup.views', url('upload/((?P<filename>.+?)/?)?$', 'upload', name='upload'))