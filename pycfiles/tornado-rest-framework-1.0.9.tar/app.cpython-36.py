# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/app.py
# Compiled at: 2018-08-22 05:08:40
# Size of source mod 2**32: 1844 bytes
from importlib import import_module
from tornado.web import Application
from rest_framework.conf import settings
from rest_framework.log import configure_logging

def url_patterns(rules):
    urlconf_module = settings.ROOT_URLCONF if rules is None else rules
    if isinstance(urlconf_module, str):
        urlconf_module = import_module(urlconf_module)
    urlpatterns = getattr(urlconf_module, 'urlpatterns', [])
    url_specs = []
    for url_spec in urlpatterns:
        if isinstance(url_spec, list):
            url_specs.extend(url_spec)
        else:
            url_specs.append(url_spec)

    return url_specs


def app_setup(rules=None, **kwargs):
    urlpatterns = url_patterns(rules)
    app_settings = dict(gzip=True,
      debug=(settings.DEBUG),
      xsrf_cookies=(settings.XSRF_COOKIES))
    app_settings.update(kwargs)
    app = Application(urlpatterns, **app_settings)
    configure_logging(settings.LOGGING)
    return app


class Application:

    def __init__(self):
        pass

    def register_route(self, pattern, handler, name=None, cache=None, **kwargs):
        route_name = handler.__name__ if name is None else name
        view_func = (handler.as_view)(name=route_name, application=self, **kwargs)
        methods = getattr(view_func, 'methods', None) or ('GET', )
        methods = set(item.upper() for item in methods)
        if isinstance(pattern, str):
            encoded_pattern = pattern.encode()
        else:
            encoded_pattern = pattern
        chosen_cache = cache
        if cache is False:
            chosen_cache = None
        new_route = Route(encoded_pattern, view_func, methods, parent=self, name=route_name, cache=chosen_cache,
          limits=(limits or self.limits))
        self.add_route(new_route)
        return handler