# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/auth_handler.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2064 bytes
__doc__ = '\nDefines an interface which all Auth handlers need to implement.\n'
from boto.plugin import Plugin

class NotReadyToAuthenticate(Exception):
    pass


class AuthHandler(Plugin):
    capability = []

    def __init__(self, host, config, provider):
        """Constructs the handlers.
        :type host: string
        :param host: The host to which the request is being sent.

        :type config: boto.pyami.Config
        :param config: Boto configuration.

        :type provider: boto.provider.Provider
        :param provider: Provider details.

        Raises:
            NotReadyToAuthenticate: if this handler is not willing to
                authenticate for the given provider and config.
        """
        pass

    def add_auth(self, http_request):
        """Invoked to add authentication details to request.

        :type http_request: boto.connection.HTTPRequest
        :param http_request: HTTP request that needs to be authenticated.
        """
        pass