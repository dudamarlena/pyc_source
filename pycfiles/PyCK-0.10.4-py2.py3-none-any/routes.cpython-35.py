# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /MyWork/Projects/PyCK/pyck/lib/routes.py
# Compiled at: 2015-02-06 20:05:39
# Size of source mod 2**32: 1140 bytes
"""Routes related utility functions"""
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