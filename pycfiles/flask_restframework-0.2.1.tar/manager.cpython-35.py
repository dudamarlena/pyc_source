# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/admin/manager.py
# Compiled at: 2017-07-25 10:25:43
# Size of source mod 2**32: 2973 bytes
from flask import jsonify, globals
from flask.app import Flask
from flask.blueprints import Blueprint
from flask_restframework.filter_backends import DefaultFilterBackend
from flask_restframework.filter_backends import OrderingBackend
from flask_restframework.pagination import DefaultPagination
from flask.helpers import url_for
from flask_restframework.model_resource import ModelResource
from flask_restframework.queryset_wrapper import QuerysetWrapper
from flask_restframework.serializer.model_serializer import ModelSerializer
from flask import globals as g

class AdminResourceWrapper:
    resource = None

    def __init__(self, resource, admin):
        self.resource = resource
        self.name = self.resource.__name__.lower()
        self.admin = admin

    def get_url(self):
        return url_for('{}.resource_{}'.format(self.admin.app.name, self.name.lower()))

    def register_url(self, app):
        app.add_url_rule('/resource/{}'.format(self.name.lower()), 'resource_{}'.format(self.name.lower()), self.view_list_resource)

    def view_list_resource(self):
        return self.resource(g.request).get(g.request)

    def to_json(self):
        return {'name': self.name, 
         'url': self.get_url()}


class Admin:
    _registered_resources = []

    def __init__(self):
        pass

    def init(self, app):
        self.app = app
        self._register_urls()

    def init_blueprint(self, app, name, import_name, url_prefix=None):
        bp = Blueprint(name, import_name, url_prefix=url_prefix)
        self.init(bp)
        app.register_blueprint(bp)

    def register_resource(self, res):
        if not isinstance(res, AdminResourceWrapper):
            self._registered_resources.append(AdminResourceWrapper(res, self))

    def _register_urls(self):
        for adminResourceWrapper in self._registered_resources:
            adminResourceWrapper.register_url(self.app)

        self.app.add_url_rule('/resources', 'resources', view_func=self.view_resources)

    def view_resources(self):
        return jsonify([arw.to_json() for arw in self._registered_resources])

    def register_model(self, modelCls):

        class S(ModelSerializer):

            class Meta:
                model = modelCls

        class Resource(ModelResource):
            serializer_class = S
            pagination_class = DefaultPagination
            filter_backends = [OrderingBackend, DefaultFilterBackend]

            def get_queryset(self):
                return QuerysetWrapper.from_model(modelCls)

        wrapper = AdminResourceWrapper(Resource, self)
        wrapper.name = modelCls.__name__.lower()
        self._registered_resources.append(wrapper)