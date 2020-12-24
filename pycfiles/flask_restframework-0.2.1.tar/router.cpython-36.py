# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/logviewer/flask_validator/router.py
# Compiled at: 2017-01-13 11:02:41
# Size of source mod 2**32: 3001 bytes
from flask.globals import request
from flask_validator.resource import BaseResource

class BaseRouter(object):

    def __init__(self, app=None):
        """
        :type app: flask.app.Flask | flask.blueprints.Blueprint
        """
        self.init_app(app)

    def init_app(self, app):
        self.app = app


class DefaultRouter(BaseRouter):
    __doc__ = '\n    You should use this class for registering Resource/ModelResource classes.\n    Example::\n\n        >>> router = DefaultRouter(app)\n        >>> router.register("/test", ResourceCls, "test")\n\n    For each register call (url, viewCls, basename)\n    It will add 2 routing rules:\n\n        * url with methods from viewCls.get_allowed_methods()\n        * url + "/<id>" with methods from viewCls.get_allowed_object_methods()\n\n    '
    METHODS = [
     'GET',
     'POST',
     'PUT',
     'PATCH',
     'DELETE',
     'HEAD',
     'OPTIONS']

    def _get_list_handler(self, request, viewCls):
        """returns handler for list route"""
        pass

    def _get_route_handler(self, func, viewCls):

        def handler(*a, **k):
            return func(viewCls(request), request, *a, **k)

        return handler

    def _iter_methods(self, viewCls, processed):
        for key, value in viewCls.__dict__.items():
            if key in processed:
                pass
            else:
                processed.append(key)
                yield (
                 key, value)

        for parentCls in viewCls.__bases__:
            yield from self._iter_methods(parentCls, processed)

    def register(self, url, viewCls, basename):
        if issubclass(viewCls, BaseResource):
            listMethods = []
            detailMethods = []
            for key, value in self._iter_methods(viewCls, []):
                if callable(value):
                    if key.upper() in self.METHODS:
                        listMethods.append(key)
                    else:
                        if key.replace('_object', '').upper() in self.METHODS:
                            detailMethods.append(key.replace('_object', ''))
                        elif hasattr(value, '_is_view_function'):
                            self.app.add_url_rule((url + value._route_part),
                              (basename + '-{}'.format(value._name_part)),
                              (self._get_route_handler(value, viewCls)),
                              methods=(value._methods))

            if listMethods:
                self.app.add_url_rule(url,
                  basename, (viewCls.as_view(basename)), methods=listMethods)
            if detailMethods:
                detailBasename = basename + '-detail'
                self.app.add_url_rule((url + '/<pk>'),
                  detailBasename, viewCls.as_view(detailBasename,
                  suffix='_object'),
                  methods=detailMethods)