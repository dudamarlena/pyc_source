# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/inspectors/routes.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 1428 bytes
"""
The current device routing table
"""
from . import inspector
from mercury_agent.inspector.hwlib.iproute2 import IPRoute2

@inspector.expose('routes')
def route_inspector():
    return IPRoute2().table


def find_default_route(routes):
    """

    :param routes:
    :return:
    """
    _defaults = []
    for route in routes:
        if route.get('destination') == 'default':
            if 'metric' not in route:
                route['metric'] = 0
            _defaults.append(route)

    if not _defaults:
        return {}
    else:
        return sorted(_defaults, key=(lambda _d: int(_d['metric'])))[0]


if __name__ == '__main__':
    from pprint import pprint
    table = route_inspector()
    pprint(table)
    pprint('----------')
    pprint(find_default_route(table))