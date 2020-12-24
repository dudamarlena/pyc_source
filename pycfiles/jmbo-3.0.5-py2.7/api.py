# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/api.py
# Compiled at: 2016-10-27 15:23:38
from django.conf.urls import url
from django.core.urlresolvers import NoReverseMatch
from tastypie.resources import ModelResource
from jmbo.models import ModelBase

class ModelBaseResource(ModelResource):

    class Meta:
        queryset = ModelBase.permitted.all()
        resource_name = 'modelbase'

    def get_resource_uri(self, bundle_or_obj=None, url_name='api_dispatch_list'):
        """The resource_uri must point to the leaf class if possible"""
        if bundle_or_obj is not None:
            try:
                leaf = bundle_or_obj.obj.as_leaf_class()
            except AttributeError:
                pass
            else:
                from jmbo.urls import v1_api
                resource = v1_api._registry.get(leaf.__class__.__name__.lower())
                if resource:
                    return resource.get_resource_uri(leaf, url_name)

        return super(ModelBaseResource, self).get_resource_uri(bundle_or_obj, url_name)

    def dehydrate(self, bundle):
        bundle.data['permalink'] = bundle.obj.get_absolute_url()
        bundle.data['image_detail_url'] = ''
        if bundle.obj.image:
            try:
                bundle.data['image_detail_url'] = bundle.obj.image_detail_url
            except AttributeError:
                pass

        return bundle