# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caowenbin/xuetangx/grpc-help/grpc_help/rules.py
# Compiled at: 2019-02-11 04:58:29
# Size of source mod 2**32: 1876 bytes
from types import MethodType
from grpc_help.utils import import_object
from grpc_help.views import StreamRpcView, AsyncStreamRpcView

class RuleMethod:

    def __init__(self, name, cls_handler):
        self.name = name
        self.cls_handler = import_object(cls_handler)


class ServiceBlueprint:

    def __init__(self, servicer, service):
        self.servicer = import_object(servicer)
        self.service = import_object(service)
        self.rule_methods = []

    def method(self, name):

        def decorator(cls):
            self.rule_methods.append(RuleMethod(name, cls))
            return cls

        return decorator

    def add_method(self, name, cls_handler):
        self.rule_methods.append(RuleMethod(name, cls_handler))


class RpcServicerBlueprint:

    def __init__(self):
        self.service_blueprints = []

    def add_service_blueprint(self, blueprint):
        self.service_blueprints.append(blueprint)

    def __iter__(self):
        return iter(self.service_blueprints)

    @staticmethod
    def _get_rpc_method(rule_method):
        if issubclass(rule_method.cls_handler, (StreamRpcView, AsyncStreamRpcView)):

            def method(*args):
                for result in rule_method.cls_handler(args[1], args[2]).__call__():
                    yield result

        else:

            def method(*args):
                return rule_method.cls_handler(args[1], args[2]).__call__()

        return method

    def register_server(self, server):
        for service_blueprint in self.service_blueprints:
            service_instance = service_blueprint.service()
            for rule_method in service_blueprint.rule_methods:
                setattr(service_instance, rule_method.name, MethodType(self._get_rpc_method(rule_method), service_instance))

            service_blueprint.servicer(service_instance, server)