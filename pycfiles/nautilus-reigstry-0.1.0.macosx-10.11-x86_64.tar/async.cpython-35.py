# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/nautilus-registry/fields/connections/async.py
# Compiled at: 2016-06-20 02:03:52
# Size of source mod 2**32: 831 bytes
from .base import BaseConnection

class AsyncConnection(BaseConnection):
    __doc__ = '\n        This Connection is very similar in function to the base class, however\n        in order to resolve the various bits of the connection, this connection\n        uses the event system to request/recieve information.\n    '

    def resolve_service(self, instance, args, info):
        """
            This function grabs the remote data that acts as the source for this
            connection by querying for the relevant fields from the event pool 
            and waiting for a reply.

            Note: it is safe to assume the target is a service object -
                strings have been coerced.
        """
        pass