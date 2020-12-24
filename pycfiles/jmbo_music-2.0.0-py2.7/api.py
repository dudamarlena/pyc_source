# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/api.py
# Compiled at: 2015-06-12 10:21:37
from django.conf.urls import url
from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie import fields
from jmbo.api import ModelBaseResource
from music.models import Track, TrackContributor

class TrackContributorResource(ModelBaseResource):

    class Meta:
        queryset = TrackContributor.permitted.all()
        resource_name = 'trackcontributor'


class TrackResource(ModelBaseResource):
    contributor = fields.ToManyField(TrackContributorResource, 'contributor', full=True)

    class Meta:
        queryset = Track.permitted.all()
        resource_name = 'track'
        filtering = {'last_played': ALL}
        ordering = [
         'last_played']