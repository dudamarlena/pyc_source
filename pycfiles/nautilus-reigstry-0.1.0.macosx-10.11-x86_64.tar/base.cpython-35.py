# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/nautilus-registry/fields/connections/base.py
# Compiled at: 2016-06-22 05:46:52
# Size of source mod 2**32: 4234 bytes
from graphene import List, with_context
from graphene.relay import ConnectionField
from ..objectTypes import ServiceObjectType
from ..objectTypes.serviceObjectType import serivce_objects
from nautilus.api.filter import args_for_model

class BaseConnection(List):
    __doc__ = '\n        A field that encapsultes a connection with another GraphQL object.\n\n        Args:\n\n            target (str or ObjectType): The target object type. If target is a\n                SerivceObjectType then the remote data lookup is automated using the\n                target object\'s meta service attribute.\n\n            relationship (str: "one" or "many"): The kind of relationship that this\n                connection encapsultes. If set to "many" the connection will result in\n                a list whereas if it is set to "one" the connection will result in the\n                object type itself.\n\n\n        Example:\n\n            For an example, see the getting started guide.\n\n    '

    def __init__(self, target, relationship='many', **kwds):
        perform_resolve = 'resolver' not in kwds and (isinstance(target, str) or issubclass(target, ServiceObjectType))
        list_wrapper = List(target)
        if hasattr(target, 'service') and hasattr(target.service, 'model'):
            kwds['args'] = args_for_model(target.service.model)
        if not perform_resolve:
            super().__init__(type=list_wrapper, **kwds)
            return
        if relationship != 'many':
            raise ValueError('single relationships are not yet supported')
        self.target = target
        self.relationship = relationship
        kwds['resolver'] = self._resolve
        super().__init__(of_type=target, **kwds)

    def resolve_service(self, args, context, info):
        """
            This function performs the actual resolution of the service.
            Not implemented in this class - left up to subclasses.
        """
        raise NotImplementedError

    @with_context
    def _resolve(self, args, context, info):
        args = query_args if isinstance(query_args, dict) else query_args.to_data_dict()
        if isinstance(self.target, str):
            if self.target in serivce_objects:
                self.target = serivce_objects[self.target]
        else:
            raise ValueError('Please provide a string designating a ' + 'ServiceObjectType as the target for ' + 'a connection.')
        return self.resolve_service(instance, args, context, info)

    def _service_name(self, target):
        try:
            return target.service.name
        except AttributeError as err:
            if isinstance(target, str):
                return target
            raise err