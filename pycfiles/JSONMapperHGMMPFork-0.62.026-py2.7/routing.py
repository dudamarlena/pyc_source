# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jsonmapper\routing.py
# Compiled at: 2012-12-05 11:56:52
from operator import attrgetter
from pyramid.httpexceptions import HTTPFound
STANDARD_VIEW_ATTRS = [{'attr': 'GET', 'request_method': 'GET'}]
STANDARD_FORM_ATTRS = [{'attr': 'GET', 'request_method': 'GET'}, {'attr': 'POST', 'request_method': 'POST'}]
JSON_HANDLER_ATTRS = [{'attr': 'ajax', 'request_method': 'POST', 'xhr': True, 'renderer': 'json'}]
JSON_FORM_ATTRS = [{'attr': 'GET', 'request_method': 'GET'}, {'attr': 'POST', 'request_method': 'POST', 'xhr': False}, {'attr': 'ajax', 'request_method': 'POST', 'xhr': True, 'renderer': 'json'}]
JSON_LINK_ATTRS = [{'attr': 'GET', 'request_method': 'GET'}, {'attr': 'ajax', 'request_method': 'POST', 'xhr': True, 'renderer': 'json'}]

class App(object):

    def __init__(self, name):
        self.name = name


class BaseRoute(object):

    def getRouteName(self, app_name, route_name=None):
        if route_name is not None:
            return route_name
        else:
            return self.name

    def setup(self, apps, config):
        raise NotImplementedError()


def redirectView(toRoute, *args, **kwargs):

    def redirect(request):
        request.fwd(toRoute, *args, **kwargs)

    return redirect


class RedirectRoute(BaseRoute):
    renderer = None

    def __init__(self, name, path_exp, to_route, *args, **kwargs):
        self.name = name
        self.path_exp = path_exp
        self.to_route = to_route
        self.route_args = args
        self.route_kwargs = kwargs

    def setup(self, apps, config):
        for app in apps:
            route_name = self.getRouteName(app.name)
            config.add_route(route_name, self.path_exp)
            view = redirectView(self.getRouteName(app.name, self.to_route), *self.route_args, **self.route_kwargs)
            config.add_view(view, route_name=route_name)


class FunctionRoute(BaseRoute):

    def __init__(self, name, path_exp, factory, view, renderer, route_attrs={}):
        self.name = name
        self.path_exp = path_exp
        self.factory = factory
        self.view = view
        self.renderer = renderer
        self.route_attrs = route_attrs

    def setup(self, apps, config):
        for app in apps:
            route_name = self.getRouteName(app.name)
            config.add_route(route_name, self.path_exp, factory=self.factory, **self.route_attrs)
            self.addView(config, route_name)

    def addView(self, config, route_name):
        config.add_view(self.view, route_name=route_name, renderer=self.renderer)


class ClassRoute(FunctionRoute):

    def __init__(self, name, path_exp, factory, view, renderer=None, view_attrs=[]):
        self.view_attrs = view_attrs
        super(ClassRoute, self).__init__(name, path_exp, factory, view, renderer)

    def addView(self, config, route_name):
        for attrs in self.view_attrs:
            attrs = attrs.copy()
            renderer = attrs.pop('renderer', self.renderer)
            config.add_view(view=self.view, route_name=route_name, renderer=renderer, **attrs)