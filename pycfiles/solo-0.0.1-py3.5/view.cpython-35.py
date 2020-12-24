# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/configurator/view.py
# Compiled at: 2016-03-29 19:16:41
# Size of source mod 2**32: 3021 bytes
import logging
from typing import List
from .config.routes import RouteItem
from aiohttp.web import Request, Response, HTTPNotFound
import venusian
log = logging.getLogger(__name__)

class http_endpoint(object):
    venusian = venusian

    def __init__(self, **settings):
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        depth = settings.pop('_depth', 0)

        def callback(scanner, name, obj):
            scanner.config.add_view(view=obj, **settings)

        info = self.venusian.attach(wrapped, callback, category='solo', depth=depth + 1)
        if info.scope == 'class' and settings.get('attr') is None:
            settings['attr'] = wrapped.__name__
        return wrapped


class http_defaults(http_endpoint):
    __doc__ = ' This object is a copy of ``pyramid.view.view_defaults``.\n\n    A class :term:`decorator` which, when applied to a class, will\n    provide defaults for all view configurations that use the class. This\n    decorator accepts all the arguments accepted by\n    :meth:`pyramid.view.view_config`, and each has the same meaning.\n\n    See :ref:`view_defaults` for more information.\n    '

    def __call__(self, wrapped):
        wrapped.__view_defaults__ = self.__dict__.copy()
        return wrapped


class PredicatedHandler:
    __slots__ = [
     'viewlist']

    def __init__(self, viewlist: List[RouteItem]):
        self.viewlist = viewlist

    def __call__(self, request: Request):
        """ Resolve predicates here.
        """
        for route_item in self.viewlist:
            for predicate in route_item.predicates:
                if not predicate(None, request):
                    log.debug('Predicate {} failed for {} {}'.format(predicate, request.method, request.path_qs))
                    break
            else:
                log.debug('{} {} will be handled by {}'.format(request.method, request.path_qs, route_item.view))
                handler = route_item.view
                if route_item.attr:
                    handler = getattr(handler(request), route_item.attr)
                    response = await handler()
                else:
                    response = await handler(request)
                if isinstance(response, Response):
                    return response
                else:
                    renderer = route_item.renderer
                    return renderer(request, response)

        log.debug('All predicates have failed for {} {}'.format(request.method, request.path_qs))
        raise HTTPNotFound()