# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/RESTinpy/adapters.py
# Compiled at: 2009-04-22 07:30:36
from django.db import models
import re

class IdentityAdapter:

    def direct(self, source):
        return dict(source)

    def inverse(self, source):
        return dict(source)


class UriAdapter:

    def __init__(self, all_resources, baseurl=''):
        self.all_resources = all_resources
        self.baseurl = baseurl

    def direct(self, source):
        if isinstance(source, models.Model):
            return self.baseurl + source.get_absolute_url()
        elif isinstance(source, dict):
            result = {}
            for (k, v) in source.items():
                result[k] = self.direct(v)

            return result
        elif isinstance(source, list) or isinstance(source, models.query.QuerySet):
            return [ self.direct(x) for x in source ]
        else:
            return source

    def inverse(self, source):
        if isinstance(source, dict):
            if 'collection' in source:
                for resource in self.all_resources:
                    regex = '/' + resource.get_url_regex() + '$'
                    args = re.match(regex, source['collection'])
                    if args:
                        source['resource'] = resource
                        source['model_class'] = resource.model_class
                        request = None
                        source['object'] = resource.get_object(request, **args.groupdict())

            return source
        elif isinstance(source, list):
            return [ self.inverse(x) for x in source ]
        else:
            return source
        return


class DirectoryUriAdapter:

    def __init__(self, all_resources, baseurl=''):
        self.all_resources = all_resources
        self.baseurl = baseurl

    def direct(self, source):
        if type(source) == dict and source.has_key('collection'):
            collection = source['collection']
            source['collection'] = None
            for resource in self.all_resources:
                if resource.model_class is collection:
                    if resource.is_directory_resource():
                        source['collection'] = self.baseurl + '/' + resource.get_url_regex()

        if type(source) == dict and source.has_key('objects'):
            for object in source['objects']:
                if type(object) == dict and object.has_key('field'):
                    for (k, v) in object['field'].items():
                        self.direct(v)

        return source

    def inverse(self, source):
        return source