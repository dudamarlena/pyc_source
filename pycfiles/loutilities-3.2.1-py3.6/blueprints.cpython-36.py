# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\flask_helpers\blueprints.py
# Compiled at: 2019-11-20 12:46:54
# Size of source mod 2**32: 2976 bytes
"""
blueprints - blueprint helpers
=================================
"""

def add_url_rules(bp, cls, decorator=None, decorator_args=[]):
    """
    add url rules to bp for class cls

    cls may define the following class attribute
        url_rules   dict {endpoint: options, ...} 
            endpoint    the endpoint for the registered URL rule
            options     tuple (url_rule[, methods[, defaults]])
                url_rule    the URL rule as string
                methods     tuple of supported methods, e.g. 'GET', 'POST'
                defaults    optional dict with defaults for other rules with the same endpoint
                            see http://werkzeug.pocoo.org/docs/0.14/routing/#werkzeug.routing.Rule
    """
    for endpoint, options in cls.url_rules.items():
        url_rule = options
        methods = ('GET', )
        defaults = {}
        if len(options) == 2:
            url_rule, methods = options
        else:
            if len(options) == 3:
                url_rule, methods, defaults = options
            if not decorator:
                view_func = cls.as_view(endpoint)
            else:
                view_func = decorator(*decorator_args)(cls.as_view(endpoint))
        bp.add_url_rule(url_rule, endpoint=endpoint, methods=methods, defaults=defaults,
          view_func=view_func)


def list_routes(app):
    """
    debug to list routes for app
    """
    from urllib import parse
    from flask import url_for
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = '[{0}]'.format(arg)

        methods = ','.join(rule.methods)
        url = url_for((rule.endpoint), **options)
        line = parse.unquote('{:50s} {:20s} {}'.format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)