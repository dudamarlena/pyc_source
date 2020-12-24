# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/star/api/urls.py
# Compiled at: 2011-10-07 22:01:57
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view
from handlers import StarHandler
star_handler = Resource(StarHandler)
urlpatterns = patterns('', url('^(?P<content_type>\\d+)/(?P<object_id>\\d+)/$', star_handler, name='star-api'), url('^(?P<content_type>\\d+)/(?P<object_id>\\d+)/(?P<star_id>\\d+)/$', star_handler, name='star-api'), url('^doc/$', documentation_view))