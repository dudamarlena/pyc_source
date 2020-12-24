# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/lib/routes.py
# Compiled at: 2015-02-06 20:05:39
# Size of source mod 2**32: 1140 bytes
__doc__ = 'Routes related utility functions'
from collections import OrderedDict

def get_routes(request):
    """Returns OrderedDict of routes available for given request
    
    :param request: Request object (normally called from controller code)
    
    :returns: OrderedDict of routes with routename as key and route url as value
    """
    routes = {}
    sorted_routes = OrderedDict()
    main_routenames = []
    app_routenames = []
    for r in request.registry.introspector.get_category('routes'):
        route = r['introspectable']
        routes[route['name']] = route['pattern']
        if '.' in route['name']:
            app_routenames.append(route['name'])
        else:
            main_routenames.append(route['name'])

    for routename in sorted(main_routenames) + sorted(app_routenames):
        sorted_routes[routename] = routes[routename]

    return sorted_routes