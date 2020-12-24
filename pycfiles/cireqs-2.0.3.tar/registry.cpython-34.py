# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cirdan/registry.py
# Compiled at: 2015-07-07 15:47:12
# Size of source mod 2**32: 2823 bytes
from __future__ import absolute_import
import inspect, itertools, re
from collections import OrderedDict

class Resource:

    def __init__(self, cls):
        self.title = cls.__name__
        self.path = '???'
        self.description = None
        self.methods = []
        self.secret = False

    def safe_title(self):
        assert hasattr(self, 'title')
        return re.sub('[^A-Za-z0-9_\\-]', '', self.title.strip().replace(' ', '_'))

    def __str__(self):
        return '%s - %s' % (self.title, self.path)


class RouteMethod:

    def __init__(self, func):
        self.verb = METHODS_TO_VERBS[func.__name__]
        self.title = self.verb
        self.description = None
        self.parameters = []
        self.return_statuses = []
        self.content_type = None
        self.requires_permission = None
        self.secret = False
        self.example_request = None
        self.example_response = None

    def __str__(self):
        return '%s: %s' % (self.verb, str(self.title))


class Parameter:

    def __init__(self, name, description, required):
        self.name = name
        self.description = description
        self.required = required

    def __str__(self):
        return '%s: %s (required = %s' % (self.name, self.description, repr(self.required))


class ReturnStatus:

    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description


METHODS_TO_VERBS = OrderedDict([
 ('on_post', 'POST'),
 ('on_get', 'GET'),
 ('on_put', 'PUT'),
 ('on_delete', 'DELETE'),
 ('on_patch', 'PATCH')])

class Registry:

    def __init__(self):
        self.api_to_resources = {}
        self.api_meta = {}
        self.resources = {}
        self.route_methods = {}

    def get(self, item):
        if inspect.isclass(item):
            if id(item) not in self.resources:
                self.resources[id(item)] = Resource(item)
            return self.resources[id(item)]
        else:
            if id(item) not in self.route_methods:
                self.route_methods[id(item)] = RouteMethod(item)
            return self.route_methods[id(item)]

    def knows_about(self, api):
        return api in self.api_to_resources

    def bind_api(self, api, resource):
        if api not in self.api_to_resources:
            self.api_to_resources[api] = []
        self.api_to_resources[api].append(resource)

    def set_api_meta(self, api, **kwargs):
        self.api_meta[api] = kwargs

    def dump(self, api):
        for resource in self.api_to_resources[api]:
            print(resource)
            for method in resource.methods:
                print('\t' + str(method))


registry = Registry()