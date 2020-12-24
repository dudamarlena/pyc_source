# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/configurator/config/routes.py
# Compiled at: 2016-03-29 18:06:29
# Size of source mod 2**32: 1733 bytes
from typing import List, Optional
from ..exceptions import ConfigurationError

class RoutesConfiguratorMixin(object):

    def add_route(self, name: str, pattern, rules=None,
                  extra_kwargs=None):
        pattern = '{}/{}'.format(self.route_prefix.rstrip('/'), pattern.lstrip('/'))
        self.routes[name] = Route(name=name, pattern=pattern, rules=rules, extra_kwargs=extra_kwargs, viewlist=[])

    def check_routes_consistency(self):
        for route_name, route in self.routes.items():
            viewlist = route.viewlist
            if not viewlist:
                raise ConfigurationError('Route name "{name}" is not associated with a view callable.'.format(name=route_name))
            for route_item in viewlist:
                if route_item.view is None:
                    raise ConfigurationError('Route name "{name}" is not associated with a view callable.'.format(name=route_name))


class RouteItem:
    __slots__ = [
     'view', 'attr', 'renderer', 'predicates']

    def __init__(self, view, attr: Optional[str], renderer, predicates):
        self.view = view
        self.attr = attr
        self.renderer = renderer
        self.predicates = predicates


class Route:
    __slots__ = [
     'name', 'pattern', 'rules', 'extra_kwargs', 'viewlist']

    def __init__(self, name: str, pattern, rules, extra_kwargs, viewlist: List[RouteItem]):
        self.name = name
        self.pattern = pattern
        self.rules = rules
        self.extra_kwargs = extra_kwargs
        self.viewlist = viewlist