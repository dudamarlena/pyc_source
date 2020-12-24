# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/video/api.py
# Compiled at: 2015-06-24 05:30:26
from django.conf.urls import url
from tastypie.resources import ModelResource
from jmbo.api import ModelBaseResource
from video.models import Video

class VideoResource(ModelBaseResource):

    class Meta:
        queryset = Video.permitted.all()
        resource_name = 'video'