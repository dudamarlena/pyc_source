# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/nautilus-registry/fields/connections/sync.py
# Compiled at: 2016-06-22 05:47:59
# Size of source mod 2**32: 4481 bytes
import nautilus
from nautilus.conventions.services import connection_service_name
from ..util import query_service
from ..objectTypes import ServiceObjectType
from .base import BaseConnection

class Connection(BaseConnection):
    __doc__ = '\n        This connection resolves data by making direct (http) requests\n        to the appropriate services.\n    '

    def resolve_service(self, args, context, info):
        """
            This function grab the remote data that acts as the source for this
            connection.

            Note: it is safe to assume the target is a service object -
                strings have been coerced.
        """
        target_service_name = self._service_name(self.target)
        if isinstance(self, ServiceObjectType):
            instance_service_name = self._service_name(self)
            connection_service = connection_service_name(target_service_name, instance_service_name)
            instance_pk = getattr(self, self.service.model.primary_key().name)
            join_filter = {instance_service_name: instance_pk}
            related = query_service(connection_service, [
             target_service_name], filters=join_filter)
            if len(related) == 0:
                return []
            join_ids = [entry[target_service_name] for entry in related]
            args['pk_in'] = join_ids
        fields = [field.attname for field in self.target.true_fields()]
        results = query_service(target_service_name, fields, filters=args)
        if len(results) == 0:
            return []
        if len(results) > 1 and self.relationship == 'one':
            raise ValueError('Inconsistent state reached: multiple entries ' + 'resolving a foreign key reference')
        if hasattr(self.target, 'auth'):
            try:
                current_user = context.current_user
            except AttributeError:
                raise Exception('User is not accessible.')

            if not current_user:
                raise nautilus.auth.AuthorizationError('User is not logged in.')
            results = [result for result in results if self.target.auth(self.target(**result), current_user.decode('utf-8'))]
        if len(results) == 0:
            return
        if self.relationship == 'one':
            return self.target(**results[0])
        return [self.target(**result) for result in results]